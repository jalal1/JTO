import service.user
import service.post
import service.relation

def loadtestdata():
    # add users
    jalal = service.user.AddUser('Jalal','jalal@mail.com')
    orhun = service.user.AddUser('Orhun','Orhun@mail.com')
    time = service.user.AddUser('Time','Time@mail.com')

    # add relations
    service.relation.UpdateRelation(jalal.id,orhun.id,2,jalal.id)
    service.relation.UpdateRelation(orhun.id,time.id,1,orhun.id)
    service.relation.UpdateRelation(jalal.id,time.id,2,jalal.id)

    # add posts
    service.post.AddPost("Hello World from Jalal!",jalal.id)
    service.post.AddPost("I am goint to the Gym today!",time.id)
    service.post.AddPost("I am not sure i like Gym!",orhun.id)

    return "Test data added successfully!!"