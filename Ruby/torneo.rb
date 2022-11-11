#===========================================================================================================================================================================
# Librerias usadas
#===========================================================================================================================================================================
require "rest-client"
require "json"
#===========================================================================================================================================================================
# Clases
#===========================================================================================================================================================================
#definimos la cantidad de participantes, como estos deben ser random pero de la primera generación
#utilizamos el número de la pokedéx nacional hasta el 151 junto a la función rand
equipo = 2.times.map {rand(1..151)}
#definimos un número k que nos servirá para contabilizar y ordenar los pokémon
k=0
#definimos una variable Pokemon que nos servirá para organizar las estadísticas y ataques de cada pokémon
class Pokemon
    attr_accessor :id, :nombre, :tipo, :stats, :movimientos 
    def initialize(id, nombre, tipo, stats, movimientos)
        @id = id
        @nombre = nombre
        @tipo = tipo
        @stats = stats
        @movimientos = movimientos
    end
end
class Relacion
    attr_accessor :normal, :fire, :water, :grass, :electric, :ice, :fighting, :poison, :ground, :flying, :psychic, :bug, :rock, :ghost, :dark, :dragon, :steel, :fairy
    def initialize(normal, fire, water, grass, electric, ice, fighting, poison, ground, flying, psychic, bug, rock, ghost, dark, dragon, steel, fairy)
        @normal=normal
        @fire=fire
        @water=water
        @grass=grass
        @electric=electric
        @ice=ice
        @fighting=fighting
        @poison=poison
        @ground=ground
        @flying=flying
        @psychic=psychic
        @bug=bug
        @rock=rock
        @ghost=ghost
        @dark=dark
        @dragon=dragon
        @steel=steel
        @fairy=fairy
    end
end
class Juego
    attr_accessor :fin, :numero_batalla
    def initialize(fin, numero_batalla)
        @fin = false
        @numero_batalla = 0
    end
    attr_accessor
    def nueva_ronda()
        @Juego.numero_batalla + 1
    end
    attr_accessor :pokemon1, :pokemon2
    def crear_jugadores(pokemon1,pokemon2)
        @pokemon1 = pokemon1
        @pokemon2 = pokemon2
    end
    def derrota()
        if pokemon1.stats["hp"]<1 and pokemon2.stats["hp"] >0
            @fin = true
            puts "el ganador es " + @Juego.pokemon1["name"].to_s
        end
        if pokemon2.stats["hp"]<1 and pokemon1.stats["hp"] >0
            @fin = true
            puts "el ganador es " + @Juego.pokemon2["name"].to_s
        end
    end
end
#=========
#===========================================================================================================================================================================
# Informacion necesaria pokemon
#===========================================================================================================================================================================
#usamos un ciclo for para poder extraer toda la información de cada participante
for i in equipo
    #debido a que algunos pokémon tienen 2 tipos y usaremos 4 movimientos por cada uno usaremos arrays para
    #hacer un pre-guardado de la información
    tipos1 = []
    mov_usados1 = []
    stats = []
    #enviamos un request a la URL para llamar a los competidores con su número
    #de pokedéx nacional y extraemos en primer lugar su nombre
    iniciales = RestClient.get('https://pokeapi.co/api/v2/pokemon/'+i.to_s)
    iniciales1 = JSON.parse(iniciales.to_str)
    nombres = iniciales1['name']
    
    #luego, con la misma información extraemos los tipos que posea cada pokemon y una lista al azar de 4 movimientos que este puede aprender por MT, tutor o por nivel
    cantidad_tipos = iniciales1['types'].length
    for item in (0...cantidad_tipos)
        tipos = iniciales1['types'][item]["type"]["name"]
        tipos1.push(tipos) 
    end
    #también tomaremos las stats para usarlas en los calculos de cada combate
    stats_pokemon = {}
    stats_pokemon["hp"] = iniciales1["stats"][0]["base_stat"]
    stats_pokemon["ataque"] = iniciales1["stats"][1]["base_stat"]
    stats_pokemon["defensa"] = iniciales1["stats"][2]["base_stat"]
    stats_pokemon["ataque_esp"] = iniciales1["stats"][3]["base_stat"]
    stats_pokemon["defensa_esp"] = iniciales1["stats"][4]["base_stat"]
    stats_pokemon["velocidad"] = iniciales1["stats"][5]["base_stat"]
    stats.push(stats_pokemon)
    #movimientos    
    num_mov = iniciales1['moves'].length
    movimientos = 4.times.map {rand(1...num_mov)}

    #de estos movimientos extraemos las url y las utilizamos para buscar el nombre en español y todos los stats necesarios        for movimiento in movimientos
    for movimiento in movimientos
        url_move = iniciales1["moves"][movimiento]["move"]["url"]
        mov_id = RestClient.get(url_move)
        mov_name = JSON.parse(mov_id.to_str)
        if mov_name["power"] != nil
            mov_usados = {}
            #nombre en español
            mov_usado = mov_name['names'][5]["name"]                
            mov_usados["nombre"] = mov_usado
            #precisión
            mov_prob = mov_name["accuracy"]
            mov_usados["precision"] = mov_prob
            #clase de daño
            mov_class = mov_name["damage_class"]["name"]
            mov_usados["clase"] = mov_class
            #tipo
            mov_tipo = mov_name["type"]["name"]                
            mov_usados["tipo"] = mov_tipo
            #daño
            mov_dano = mov_name["power"]
            mov_usados["dano"] = mov_dano
            mov_usados1.push(mov_usados)
            
        end            
    end
    k = k + 1
    instance_variable_set("@Pokemon_#{k}",Pokemon.new(k,nombres,tipos1,stats,mov_usados1))      
end
#===========================================================================================================================================================================
# Información necesaria juego
#===========================================================================================================================================================================
tipos_posibles = ["normal","fire","water","grass","electric","ice","fighting","poison","ground","flying","psychic","bug","rock","ghost","dark","dragon","steel","fairy"]
rel_parcial = []
$rel_danos = []
for tipo in tipos_posibles
    rel={}
    tipos = RestClient.get("https://pokeapi.co/api/v2/type/"+tipo.to_s)
    tipos1 = JSON.parse(tipos.to_str)
    rel["nombre"] = tipo.to_s
    rel["doble"]= tipos1['damage_relations']["double_damage_to"]
    rel["mitad"]= tipos1['damage_relations']["half_damage_to"]
    rel["nada"]= tipos1['damage_relations']["no_damage_to"]
    rel_parcial.push(rel)
end

for item in rel_parcial
    rel = {}
    rel["nombre"] = rel_parcial[rel_parcial.find_index(item)]["nombre"]
    rel["doble"] = []
    for debilidad in rel_parcial[rel_parcial.find_index(item)]["doble"]
        rel["doble"].push(debilidad["name"])
    end
    rel["mitad"] = []
    for debilidad in rel_parcial[rel_parcial.find_index(item)]["mitad"]
        rel["mitad"].push(debilidad["name"])
    end
    rel["nada"] = []
    for debilidad in rel_parcial[rel_parcial.find_index(item)]["nada"]
        rel["nada"].push(debilidad["name"])
    end
    $rel_danos.push(rel)
end

#===========================================================================================================================================================================
# Funciones juego
#===========================================================================================================================================================================

def buscar_mod(tipo)
    for item in $rel_danos
        if item["nombre"].match(tipo)
            dano = item
        end
    end
    dano
end

# esta def toma el daño total y le aplica los modificadores elementales
def mod_dano(dmg,mult,elemento, tipo)
    #existe un modificador de 1.5 en caso de atacar con un movimiento del mismo tipo que el del pokemon
    if elemento.to_s == "true"
        dmg = dmg*1.5
    else
        dmg = dmg
    end
    j = buscar_mod(tipo)
    nada = []
    mult.each do |item|
        nada.push(j["nada"].include? item)
    end
    mitad = []
    mult.each do |item|
        mitad.push(j["mitad"].include? item)
    end
    doble = []
    mult.each do |item|
        doble.push(j["doble"].include? item)
    end

    if doble.include? true
        dmg = dmg.to_f*2.to_f
        dmg
    end
    
    if mitad.include? true
        dmg = dmg.to_f*0.5.to_f
        dmg
    end

    if nada.include? true
        dmg = dmg.to_f*0.to_f
        dmg
    end
    dmg.ceil(0)
end
#esta def toma los 2 pokemones que están peleando, siendo x quien ataca e y el atacado
def ataque(x,y)
    result = []
    mult = y.tipo
    move = x.movimientos[rand(0...x.movimientos&.length)]
    if move != nil
        if move["clase"] == "physical"
            if move["dano"] != nil
                dmg =  ((8*move["dano"].to_f)*(x.stats[0]["ataque"].to_f/y.stats[0]["defensa"].to_f))/50.to_f
                puts x.nombre.to_s+ " usa " + move["nombre"].to_s + " contra " + y.nombre.to_s
                elemento = x.tipo.include? move["tipo"]
                tipo = move["tipo"]
                result.push(elemento, dmg, tipo)
            end        
        elsif move["clase"] == "special"
            if move["dano"] != nil
                dmg =  ((8*move["dano"].to_f)*(x.stats[0]["ataque_esp"].to_f/y.stats[0]["defensa_esp"].to_f))/50.to_f
                puts x.nombre.to_s+ " usa " + move["nombre"].to_s + " contra " + y.nombre.to_s
                elemento = x.tipo.include? move["tipo"]
                tipo = move["tipo"]
                result.push(elemento, dmg, tipo)
            end
        end
    elsif move == nil
        puts x.nombre.to_s + " falló horriblemente"
    end
    puts mod_dano(dmg,mult,elemento,tipo)
end
#puts @Pokemon_1.inspect

# x=@Pokemon_1
# y=@Pokemon_2
# k=0
# batalla = [x,y]
# competidores = []
# batalla.each do |pokemon|
#     competidor = {}
#     k = k + 1
#     competidor["competidor_#{k}"] = pokemon.nombre
#     competidor["hp"] = pokemon.stats[0]["hp"]
#     competidores.push(competidor)
# end
# puts competidores[1]
# def duelo(x,y)
#     competidores = {}
    
#     tiktak = 0
    
#     until hp.include? 0 == true
#         hp[0] = hp[0]-10
#         tiktak = tiktak + 1
#         if tiktak % 2 == 0
#             puts par = x,y
#         else
#             puts impar = y,x
#         end
#         sleep 2
#         puts " "
#     end
# end
#puts turno(@Pokemon_1,@Pokemon_2)
