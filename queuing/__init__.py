from otree.api import *



doc = ""

class C(BaseConstants):
    NAME_IN_URL = 'queue'
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 1
    ENDOWMENT = cu(100)
    
class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    ##kept = models.CurrencyField(min = 0, max = C.ENDOWMENT,label = 'La cantidad de dinero a quedarse',)
    pass 

class Player(BasePlayer):
    desired_position = models.IntegerField(label='Desired position: ')
    old_id = models.IntegerField()
    new_id = models.IntegerField()
    offer = models.CurrencyField(label = 'Offer :',min = 0,max=C.ENDOWMENT,initial=0)
    message = models.StringField(label = 'Message :')
    pass


# FUNCTIONS

def live_method(player, choice):
    group = player.group
    my_id = player.id_in_group
    response = dict(my_id = my_id, choice = choice)
    return {0: response}

def desired_position_choices(player):
    
    return range(1,player.id_in_group,1)

def my_dict(subsession):
    return dict(a=[1,2], b=[3,4])
    
def set_id(group):
    for p in group.get_players():
        p.payoff = 100

'''
def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = group.kept
    p2.payoff = C.ENDOWMENT - group.kept
'''

# PAGES

class ShufflePage(WaitPage):

    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        matrix_old = subsession.get_group_matrix()

        for p in subsession.get_players():
            p.old_id = p.id_in_group
            #print("subsession.get_players()", p)

        print("Posiciones antiguas: ",matrix_old)
        subsession.group_randomly()
        matrix_new = subsession.get_group_matrix()
        print("Posiciones nuevas despues del shuffle: ",matrix_new)
class Pag1(Page):
    form_model = 'player'
    form_fields = ['desired_position','offer','message']

    @staticmethod
    def live_method(player, data_sent):
        if (data_sent['type'] == 'offer'):
            
            group = player.group
            fromm = player.id_in_group
            to = data_sent['to']
            response = dict(type = 'offer',value = '0', to = to, fromm = fromm)
            print("Usuario de posicion ",fromm," envio una oferta a usuario de posicion:", to)
            print("La matriz es: ",player.subsession.get_group_matrix())
            return {to: response}
        
        
        elif ( data_sent['type'] == "response"):
            if (data_sent['value'] == True):
                print("Se acepto la peticion de cambio")
                ##Se intrecambian los id de los usuarios
                group_matrix = player.subsession.get_group_matrix()
                print("Matriz de posiciones actual: ",group_matrix, " Ronda: ", player.round_number," Remitente: ",data_sent['to']," Emisor: ",data_sent['fromm'])
                pos_user1 = data_sent['to']-1  ## remitente
                pos_user2 = data_sent['fromm']-1 ##emisor
                
                aux = group_matrix[player.round_number-1][pos_user1]
                group_matrix[player.round_number-1][pos_user1] = group_matrix[player.round_number-1][pos_user2]
                group_matrix[player.round_number-1][pos_user2] = aux
                print("Matriz de posiciones despues de aceptar: ",group_matrix)
                
                player.subsession.set_group_matrix(group_matrix)

                print("player.id_in_group: ",player.id_in_group)
                response = dict(type = 'response',value = True, to=data_sent['to'], fromm = data_sent['fromm'])
                
                #Enviar mensaje a los 2 usuarios involucrados
                return {data_sent['fromm']: response,data_sent['to']:dict(type='update_message',value='acept',to=data_sent['fromm'], fromm = data_sent['to'])}
            elif (data_sent['value'] == False):
                response = dict(type = 'response',value = False, to=data_sent['to'], fromm = data_sent['fromm'])
                #print("Se rechazo la peticion de cambio")
                print("Usuario de posicion ",data_sent['fromm'], " rechazo la oferta de usuario de posicion ", data_sent['to'])
                return {data_sent['to']: response,data_sent['fromm']:dict(type='update_message',value='reject',to=data_sent['to'], fromm = data_sent['fromm'])}
        elif(data_sent['type'] == 'cancel'):
            print("Se envio una cancelacion al usuario de posicion ",data_sent['to'], " desde la posicion ",data_sent['fromm']  )
            return {data_sent['to']: dict(type = 'cancel', value = 0,to = data_sent['to'],fromm = data_sent['fromm'])}
        
    pass
class Pag2(Page):
    pass

    #form_model = 'group'
    #form_fields = ['kept']

    #@staticmethod
    #def is_displayed(player: Player):
    #    return player.id_in_group == 1

#class ResultsWaitPage(WaitPage):
#    after_all_players_arrive = set_payoffs

page_sequence = [ShufflePage,Pag1,Pag2]
