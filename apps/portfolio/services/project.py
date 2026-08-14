from apps.portfolio.models import PortfolioProject


def create_portfolio_project(**data):
    return PortfolioProject.objects.create(**data)


def update_portfolio_project(project, **data):
    for field, value in data.items():
        setattr(project, field, value)

    project.save()
    return project
