CONTENT_EDITOR_GROUP = "Editor de contenido"
CONTACT_MANAGER_GROUP = "Gestor de contacto"

CONTENT_EDITOR_PERMISSIONS = {
    "site": {
        "view_siteconfiguration",
        "change_siteconfiguration",
        "view_navigationitem",
        "add_navigationitem",
        "change_navigationitem",
    },
    "businesses": {
        "view_business",
        "add_business",
        "change_business",
    },
    "catalog": {
        "view_product",
        "add_product",
        "change_product",
        "view_productfeature",
        "add_productfeature",
        "change_productfeature",
        "view_productimage",
        "add_productimage",
        "change_productimage",
    },
    "portfolio": {
        "view_portfolioproject",
        "add_portfolioproject",
        "change_portfolioproject",
    },
    "blog": {
        "view_blogpost",
        "add_blogpost",
        "change_blogpost",
    },
}

CONTACT_MANAGER_PERMISSIONS = {
    "contact": {
        "view_contactmessage",
        "change_contactmessage",
    },
}
