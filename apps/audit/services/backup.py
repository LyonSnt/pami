import os
import subprocess
from dataclasses import dataclass
from tempfile import TemporaryFile

from django.db import connections
from django.utils import timezone


class DatabaseBackupError(Exception):
    pass


@dataclass
class DatabaseBackupResult:
    file: object
    filename: str
    size: int


def create_database_backup(*, database_alias="default", timeout=120):
    database = connections[database_alias].settings_dict
    backup_file = TemporaryFile(mode="w+b")
    environment = os.environ.copy()
    environment["PGPASSWORD"] = database.get("PASSWORD", "")

    command = [
        "pg_dump",
        "--format=custom",
        "--compress=6",
        "--no-owner",
        "--no-acl",
        "--host",
        str(database.get("HOST") or "localhost"),
        "--port",
        str(database.get("PORT") or 5432),
        "--username",
        str(database.get("USER") or ""),
        str(database.get("NAME") or ""),
    ]

    try:
        completed = subprocess.run(
            command,
            stdout=backup_file,
            stderr=subprocess.PIPE,
            env=environment,
            check=False,
            timeout=timeout,
        )
    except FileNotFoundError as error:
        backup_file.close()
        raise DatabaseBackupError(
            "El servidor no tiene disponible la herramienta pg_dump."
        ) from error
    except subprocess.TimeoutExpired as error:
        backup_file.close()
        raise DatabaseBackupError(
            "El respaldo superó el tiempo máximo permitido."
        ) from error

    if completed.returncode != 0:
        backup_file.close()
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise DatabaseBackupError(
            detail or "PostgreSQL no pudo generar el respaldo."
        )

    size = backup_file.tell()
    backup_file.seek(0)
    if size < 5 or backup_file.read(5) != b"PGDMP":
        backup_file.close()
        raise DatabaseBackupError(
            "PostgreSQL produjo un archivo de respaldo no válido."
        )
    backup_file.seek(0)

    timestamp = timezone.localtime().strftime("%Y-%m-%d_%H%M%S")
    return DatabaseBackupResult(
        file=backup_file,
        filename=f"pami_db_{timestamp}.dump",
        size=size,
    )
