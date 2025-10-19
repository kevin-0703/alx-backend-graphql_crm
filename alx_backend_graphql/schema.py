import graphene
from crm.schema import CRMQuery

class Query(CRMQuery, graphene.ObjectType):
    pass  # You can add project-wide queries here if needed

schema = graphene.Schema(query=Query)
