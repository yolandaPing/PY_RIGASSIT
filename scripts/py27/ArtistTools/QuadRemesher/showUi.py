
import QuadRemesher.QuadRemesher as QuadRemesher
import production.usage_mongodb

@production.usage_mongodb.Usage('Quad Remesher', dept='rig')
def showUI():

    QuadRemesher.QuadRemesher()

