from otree.api import *
#from otree.db import models
import csv


import pandas as pd

datos_csv = pd.read_csv('config.csv', dtype={'round_number': 'int64'})
# Convierte max_round de numpy.int64 a int
max_round = datos_csv['round_number'].iloc[-1]

# Averigua el tipo de dato de max_round
print("rondas_maximas: ", max_round)
tipo_de_dato_max_round = type(max_round)
print("El tipo de dato de max_round es:", tipo_de_dato_max_round)
max_players_per_group = int(datos_csv['players_per_group'].max())
print("El valor máximo de 'players_per_group' es:", max_players_per_group)
request_and_exchangue_data = []
'''
request_and_exchangue_data_element = 
{
	"requester" : {"participant_code":"participant_code" , "player_id": "player_id", "position": "position", "offer":"offer", "message":"message"}
	"responder" : {"participant_code":"participant_code" , "player_id": "player_id", "position": "position"}
	"exchangue_status" : {"timestamp":"timestamp", "exchange_unique_id":"exchange_unique_id", "exchange_result":"exchange_result" (cancel, reject, accept)}
	"session_code" :"session_code"  
	"id_in_subsession" : "id_in_subsession"

}

'''

class C(BaseConstants):
    NAME_IN_URL = 'queue'
    PLAYERS_PER_GROUP = max_players_per_group
    NUM_ROUNDS = int(max_round)
    ENDOWMENT = cu(100)


def creating_session(self):
    swap_method = datos_csv["swap_method"][self.round_number-1]
    random_group = datos_csv["random_group"][self.round_number-1]
    players_per_group = datos_csv["players_per_group"][self.round_number-1]
    block = datos_csv["block"][self.round_number-1]
    messaging_boolean = datos_csv["messaging"][self.round_number-1]
    print("messaging : ", messaging_boolean)
    practice = datos_csv["practice"][self.round_number-1]
    endow = datos_csv["endow"][self.round_number-1]
    endow_token = datos_csv["endow_token"][self.round_number-1]
    value = datos_csv["value"][self.round_number-1]
    cost = datos_csv["cost"][self.round_number-1]
    offer_limit = datos_csv["offer_limit"][self.round_number-1]
    total_transfer = 0
    history_of_send_request = ""
    history_of_received_request = ""
    initial_position = 0

    for player in self.get_players():
            player.swap_method = swap_method
            player.random_group = random_group
            player.players_per_group = players_per_group
            player.block = block
            player.messaging_boolean = messaging_boolean
            player.practice = practice
            player.endow = endow
            player.endow_token = endow_token
            player.total_transfer = total_transfer
            player.value = value
            player.cost = cost
            player.offer_limit = offer_limit
            player.history_of_send_request = history_of_send_request
            player.history_of_received_request = history_of_received_request
            initial_position = initial_position
    
    print("session actual: ", self.round_number)
    print("Messaging", messaging_boolean)
    print("swap method", swap_method)

    

class Subsession(BaseSubsession):
    
    pass

class Group(BaseGroup):
    ##kept = models.CurrencyField(min = 0, max = C.ENDOWMENT,label = 'La cantidad de dinero a quedarse',)
    pass 

class Player(BasePlayer):
    swap_method = models.CharField(label='Swap Method',)
    players_per_group = models.IntegerField(label='Swap Method',)
    block = models.IntegerField(label='Swap Method',)
    messaging_boolean = models.BooleanField(label='messaging_boolean',)
    practice = models.BooleanField(label='Swap Method',)
    endow = models.FloatField(label='Swap Method',)
    endow_token = models.FloatField(label='Endow_tok',)
    total_transfer = models.FloatField(initial=0)
    #endow_token = models.IntegerField(label='Endow token')
    history_of_send_request = models.StringField(initial="")
    history_of_received_request = models.StringField(initial="")
    initial_position = models.IntegerField()

    desired_position = models.IntegerField(label='Desired position: ', blank=True)
    old_id = models.IntegerField()
    new_id = models.IntegerField()
    offer = models.CurrencyField(label = 'Offer :',min = 0,max=C.ENDOWMENT,initial=0, blank=True)
    message = models.StringField(label = 'Message :', blank=True)
    token = models.IntegerField(label = 'Tokens: ', blank=True)
    pass


# FUNCTIONS

def live_method(player, choice):
    group = player.group
    my_id = player.id_in_group
    response = dict(my_id = my_id, choice = choice)
    return {0: response}

def desired_position_choices(player):
    return range(1,player.id_in_group,1)
def token_choices(player):
    return range(0,datos_csv["endow_token"][player.round_number-1]+1,1)

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

class WelcomePage(Page):
    @staticmethod
    def is_displayed(player):
        print("round number: ", player.round_number)
        
        return player.round_number == 1
    pass

class WaitPage1(WaitPage):

    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        matrix_old = subsession.get_group_matrix()

        for p in subsession.get_players():
            p.old_id = p.id_in_group
            #print("subsession.get_players()", p)

        #print("Posiciones antiguas: ",matrix_old)
        randomly = datos_csv["random_group"][subsession.round_number-1]
        print("Random group: ", randomly)
        if (randomly == True):
            subsession.group_randomly()
            print("shuffle hecho")
        for player in subsession.get_players():
            player.initial_position = player.id_in_group
        matrix_new = subsession.get_group_matrix()
        print("Posiciones nuevas despues del shuffle: ",matrix_new)

class InstructionPage(Page):
    @staticmethod
    def is_displayed(player):
        print("round number: ", player.round_number)
        
        return player.round_number == 1
    pass
   

class DecisionPage(Page):

    @staticmethod
    def is_displayed(player):
        
        
        return 1
    
    form_model = 'player'
    def get_form_fields(self):
        if (self.messaging_boolean and self.swap_method == 'trade'):
            print("mensajes + trade")
            return ['desired_position', 'offer', 'message']
        elif (not self.messaging_boolean and self.swap_method == 'trade'):
            print("Sin mensajes + trade")
            return ['desired_position', 'offer']
        elif (self.messaging_boolean and self.swap_method == 'swap'):
            print("mensajes + swap")
            return ['desired_position', 'message']
        elif (not self.messaging_boolean and self.swap_method == 'swap'):
            print("sin mensajes + swap")
            return ['desired_position']
        elif (self.messaging_boolean and self.swap_method == 'token'):
            print("mensajes + token")
            return ['desired_position', 'token', 'message']
        elif (self.messaging_boolean and self.swap_method == 'token'):
            print("sin mensajes + token")
            return ['desired_position', 'token']

    @staticmethod
    def live_method(player, data_sent):
        if (data_sent['type'] == 'offer'):
            
            group = player.group
            fromm = player.id_in_group
            message_to_send = data_sent['message_to_send']
            print(message_to_send)
            points_offer = data_sent['points_offer']
            token_offer_message = data_sent['token_offer_message']
            print("token_offer_message: ", data_sent['token_offer_message'])
            to = data_sent['to']
            response = dict(type = 'offer',value = '0', to = to, fromm = fromm, points_offer = points_offer, message_to_send = message_to_send, token_offer_message = token_offer_message)
            print("Usuario de posicion ",fromm," envio una oferta a usuario de posicion:", to)
            print("La matriz es: ",player.subsession.get_group_matrix())
            return {to: response}
        
        #cuando responden al que envia la peticion afirmativamente
        elif ( data_sent['type'] == "response"):
            # Si el intercambio se acepto
            if (data_sent['value'] == True):
                print("Se acepto la peticion de cambio")
                ##Se intrecambian los id de los usuarios
                group_matrix = player.subsession.get_group_matrix()
                print("Matriz de posiciones actual: ",group_matrix, " Ronda: ", player.round_number," Remitente: ",data_sent['to']," Emisor: ",data_sent['fromm'])
                pos_user1 = data_sent['to']-1  ## remitente
                pos_user2 = data_sent['fromm']-1 ##emisor
                print("matriz de grupos: ",group_matrix)
                
                aux = group_matrix[0][pos_user1]
                group_matrix[0][pos_user1] = group_matrix[0][pos_user2]
                group_matrix[0][pos_user2] = aux
                
                #aux = group_matrix[player.round_number-1][pos_user1]
                #group_matrix[player.round_number-1][pos_user1] = group_matrix[player.round_number-1][pos_user2]
                #group_matrix[player.round_number-1][pos_user2] = aux


                print("Matriz de posiciones despues de aceptar: ",group_matrix)
                
                player.subsession.set_group_matrix(group_matrix)

                print("player.id_in_group: ",player.id_in_group)

                #Actualziar informacion de participantes
                if(data_sent['swap_method'] == 'trade'):
                    print("swap_method trade", player.endow , data_sent['points_offer'])
                if(data_sent['swap_method'] == 'swap'):
                    print("swap_method _ swap", player.endow , data_sent['points_offer'])
                if(data_sent['swap_method'] == 'token'):
                    print("swap_method _ token", player.endow , data_sent['token_offer_message'])
                    

                
                print("recibir datos")
                response = dict(type = 'response',value = True, to=data_sent['to'], fromm = data_sent['fromm'], message_to_send = data_sent['message_to_send'], token_offer_message = data_sent['token_offer_message'], points_offer = data_sent['points_offer'] )
                print("enviar datos")
                #Enviar mensaje a los 2 usuarios involucrados
                return {data_sent['fromm']: response,data_sent['to']:dict(type='update_message',value='acept',to=data_sent['fromm'], fromm = data_sent['to'])}
            
            # Si el intercambio se rechaza
            elif (data_sent['value'] == False):
                response = dict(type = 'response',value = False, to=data_sent['to'], fromm = data_sent['fromm'])
                #print("Se rechazo la peticion de cambio")
                print("Usuario de posicion ",data_sent['fromm'], " rechazo la oferta de usuario de posicion ", data_sent['to'])
                return {data_sent['to']: response,data_sent['fromm']:dict(type='update_message',value='reject',to=data_sent['to'], fromm = data_sent['fromm'])}
        elif(data_sent['type'] == 'cancel'):
            print("Se envio una cancelacion al usuario de posicion ",data_sent['to'], " desde la posicion ",data_sent['fromm']  )
            return {data_sent['to']: dict(type = 'cancel', value = 0,to = data_sent['to'],fromm = data_sent['fromm'])}
        
        elif ( data_sent['type'] == "save_history"):
            player.history_of_send_request = data_sent['send_request']
            player.history_of_received_request = data_sent['received_request']
            print("Guardar historial: ",player.id_in_group, player.history_of_received_request)

        elif( data_sent['type'] == 'update_total_transfer' ):
            #actualizar la trasferencia total        
            player.total_transfer = player.total_transfer + float(data_sent['value'])
            print("total_fransfer: ", player.total_transfer)
            print("player payoff(in total transfer): ", player.payoff )
        elif (data_sent['type'] == 'update_payoff'):
            if(player.swap_method == "token"):
                player.payoff = player.endow_token + player.total_transfer
                print("player payoff token: ", player.payoff )
            if(player.swap_method == "trade"):
                player.payoff = player.endow - player.total_transfer
                print("player payoff points: ", player.payoff )
        
    pass
class ResultPage(Page):
    pass

    #form_model = 'group'
    #form_fields = ['kept']

    #@staticmethod
    #def is_displayed(player: Player):
    #    return player.id_in_group == 1

#class ResultsWaitPage(WaitPage):
#    after_all_players_arrive = set_payoffs

import json
class FinalPage(Page):
    
    @staticmethod
    def is_displayed(player):
        #if (player.round_number == max_round):
            #request_and_exchangue_data.append(["numero",player.id_in_group,player.round_number])
            #nombre_archivo = "request_and_exchangue_data.json"
            # Guardar la lista en el archivo JSON
            #with open(nombre_archivo, "w") as archivo_json:
            #    json.dump(request_and_exchangue_data, archivo_json)

            #print(f"Los datos se han guardado en {nombre_archivo}")
        
        return player.round_number == max_round
    pass
    
page_sequence = [WelcomePage, InstructionPage, WaitPage1, DecisionPage, ResultPage, FinalPage]
