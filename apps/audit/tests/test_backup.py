import subprocess
from unittest.mock import patch

from django.test import TestCase

from apps.audit.services.backup import (
    DatabaseBackupError,
    create_database_backup,
)


class DatabaseBackupServiceTests(TestCase):

    def test_pg_dump_creates_valid_custom_archive(self):
        backup = create_database_backup()

        self.assertEqual(backup.file.read(5), b"PGDMP")
        self.assertGreater(backup.size, 5)
        backup.file.close()

    @patch("apps.audit.services.backup.subprocess.run")
    def test_backup_uses_custom_format_without_exposing_password(self, run):
        def write_backup(command, *, stdout, **kwargs):
            stdout.write(b"PGDMP-valid-backup")
            return subprocess.CompletedProcess(command, 0, stderr=b"")

        run.side_effect = write_backup

        backup = create_database_backup()

        command = run.call_args.args[0]
        environment = run.call_args.kwargs["env"]
        self.assertIn("--format=custom", command)
        self.assertIn("--no-owner", command)
        self.assertNotIn(environment.get("PGPASSWORD", ""), command)
        self.assertTrue(backup.filename.startswith("pami_db_"))
        self.assertTrue(backup.filename.endswith(".dump"))
        backup.file.close()

    @patch("apps.audit.services.backup.subprocess.run")
    def test_invalid_pg_dump_output_is_rejected(self, run):
        def write_invalid_backup(command, *, stdout, **kwargs):
            stdout.write(b"invalid")
            return subprocess.CompletedProcess(command, 0, stderr=b"")

        run.side_effect = write_invalid_backup

        with self.assertRaisesMessage(
            DatabaseBackupError,
            "archivo de respaldo no válido",
        ):
            create_database_backup()
