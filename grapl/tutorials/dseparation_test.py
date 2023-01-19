import grapl.dsl as dsl
import dsep
grapl_obj = dsl.GraplDSL()

dag_1 = ' "Test"; \
    x; z; y; \
    x <-> z; \
    x -> z; \
    z -> y; '

daggrapl_1 = grapl_obj.readgrapl(dag_1)
print(dsep.dsep('x','y','z',daggrapl_1))


dag_2 = ' "Test"; \
    x; z; y; \
    x <-> z; \
    x -> z; \
    y -> z; '

daggrapl_2 = grapl_obj.readgrapl(dag_2)
print(dsep.dsep('x','y','z',daggrapl_2))