puts "Cargando torneo"
puts " "
puts " "
puts " "
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
equipo = 8.times.map {rand(1...151)}
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
    movimientos = 10.times.map {rand(1...num_mov)}

    #de estos movimientos extraemos las url y las utilizamos para buscar el nombre en español y todos los stats necesarios        for movimiento in movimientos
    for movimiento in movimientos
        if iniciales1["moves"][movimiento]["move"]["url"] != nil
            url_move = iniciales1["moves"][movimiento]["move"]["url"]
        end
            mov_id = RestClient.get(url_move)
        mov_name = JSON.parse(mov_id.to_str)
        h=0
        if h < 4
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
                h = h + 1 
            end  
        end          
    end
    k = k + 1
    ## adjuntamos todo a la clase Pokemon que será utilizada durante todo el script
    instance_variable_set("@Pokemon_#{k}",Pokemon.new(k,nombres,tipos1,stats,mov_usados1))      
end
#===========================================================================================================================================================================
# Información necesaria juego
#===========================================================================================================================================================================
# Acá extraemos los datos de los tipos elementales del juego, de esta forma podemos buscar por ataque las debilidades y fortalezas
tipos_posibles = ["normal","fire","water","grass","electric","ice","fighting","poison","ground","flying","psychic","bug","rock","ghost","dark","dragon","steel","fairy"]
rel_parcial = []
$rel_danos = []
# acá extraemos la información de pokeAPI
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
#acá establecemos una tabla final que nos servirá para buscar los daños mediante una funcion
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
#esta funcion busca los modificadores de daño para cada ataque utilizado y lo guarda en arrays
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
    #estos son los modificadores de daño
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
    #finalmente devuelve el daño redondéandolo hacia arriba
    dmg.ceil(0)
end

#esta def toma los 2 pokemones que están peleando, siendo x quien ataca e y el atacado
def ataque(x,y)
    result = []
    mult = y.tipo
    move = x.movimientos[rand(0...x.movimientos.length.to_int)]
    if move != nil
        if move["clase"] == "physical"
            # en caso de ser un ataque físico calculamos el daño utilizando la función de la primera generación y considerando
            # que todos los pokemon están con un multiplicador de nivel 10
            if move["dano"] != nil
                dmg =  ((10*move["dano"].to_f)*(x.stats[0]["ataque"].to_f/y.stats[0]["defensa"].to_f))/50.to_f
                puts x.nombre.to_s+ " usa " + move["nombre"].to_s + " contra " + y.nombre.to_s
                elemento = x.tipo.include? move["tipo"]
                tipo = move["tipo"]
                result.push(elemento, dmg, tipo)
                sleep 1
            end        
        elsif move["clase"] == "special"
            # lo mismo aplica para el ataque y la defensa especial
            if move["dano"] != nil
                dmg =  ((10*move["dano"].to_f)*(x.stats[0]["ataque_esp"].to_f/y.stats[0]["defensa_esp"].to_f))/50.to_f
                puts x.nombre.to_s+ " usa " + move["nombre"].to_s + " contra " + y.nombre.to_s
                elemento = x.tipo.include? move["tipo"]
                tipo = move["tipo"]
                result.push(elemento, dmg, tipo)
                sleep 1
            end
        end
    elsif move == nil #en algunos casos el programa confunde ataques, cuando esto pasa lo ponemos como un fallo
        puts x.nombre.to_s + " falló horriblemente"
    end
    # aplicamos los modificadores de daño que tenemos de la función anterior
    mod_dano(dmg,mult,elemento,tipo)
end
# esta def considera el atributo velocidad y dice que pokemon parte primero
def primero (x,y)
    if x.stats[0]["velocidad"] > y.stats[0]["velocidad"]
        return x
    elsif x.stats[0]["velocidad"] < y.stats[0]["velocidad"]
        return y
    else
        return x
    end
end
# Acá hay un error que no supe solucionar, pero creo que es el más problemático

# esta funcion contempla cada turno en el combate, separa a los pokemon por local y visita
# para almacenar los datos de forma distinta a la clase

# Use dos def para minimizar los problemas que se generan en este loop
def local_parte (x,y)
    local = x
    visita = y
    monitor = 1 
    until monitor <= 0
        if local.stats[0]["hp"] >= 0
            if visita.stats[0]["hp"] >= 0
                visita.stats[0]["hp"] = visita.stats[0]["hp"].to_int-ataque(local,visita)
                puts "y baja su hp a " + visita.stats[0]["hp"].to_s
                sleep 1
                puts " "
                monitor = visita.stats[0]["hp"]
                if visita.stats[0]["hp"] >= 0
                    if local.stats[0]["hp"] >= 0
                        local.stats[0]["hp"] = local.stats[0]["hp"].to_int-ataque(visita,local)
                        puts "y baja su hp a " + local.stats[0]["hp"].to_s
                        sleep 1
                        puts " "
                        monitor = local.stats[0]["hp"]
                        if local.stats[0]["hp"] < 0
                            monitor = local.stats[0]["hp"]
                            ganador = visita
                        end
                    else
                        monitor = local.stats[0]["hp"]
                        ganador = visita
                    end
                else
                    monitor = visita.stats[0]["hp"]
                    ganador = local
                end
            else
                monitor = visita.stats[0]["hp"]
                ganador = local
            end
        elsif local.stats[0]["hp"] < 0
            monitor = local.stats[0]["hp"]
            ganador = visita
        end
        if monitor < 0
            break
        end
    end
    resultado = [monitor, ganador]
end

def visita_parte(x,y)
    local = x
    visita = y
    monitor = 1 
    until monitor <= 0
        if visita.stats[0]["hp"] >= 0
            if local.stats[0]["hp"] >= 0
                local.stats[0]["hp"] = local.stats[0]["hp"].to_int-ataque(visita,local)
                puts "y baja su hp a " + local.stats[0]["hp"].to_s
                sleep 1
                puts " "
                monitor = local.stats[0]["hp"]

                if local.stats[0]["hp"] >= 0
                    if visita.stats[0]["hp"] >= 0
                        visita.stats[0]["hp"] = visita.stats[0]["hp"].to_int-ataque(local,visita)
                        puts "y baja su hp a " + visita.stats[0]["hp"].to_s
                        sleep 1
                        puts " "
                        monitor = visita.stats[0]["hp"]
                        if visita.stats[0]["hp"] < 0
                            monitor = visita.stats[0]["hp"]
                            ganador = local
                        end
                    else
                        monitor = visita.stats[0]["hp"]
                        ganador = local
                    end
                else
                    monitor = local.stats[0]["hp"]
                    ganador = visita
                end
            else
                monitor = local.stats[0]["hp"]
                ganador = visita
            end
        elsif visita.stats[0]["hp"] < 0
            monitor = visita.stats[0]["hp"]
            ganador = local
        end
        
        if monitor < 0
            break
        end    
    end
    resultado = [monitor, ganador]
end

def turno(x,y)
    local = x
    visita = y
    # usamos la def para ver quien parte
    quien = primero(local,visita).nombre
    if primero(local,visita).nombre == local.nombre
        z =local_parte(local, visita)
    elsif primero(local,visita).nombre == visita.nombre
        z = visita_parte(local, visita)
    end
end

def combate(x,y)
    puts " "
    puts " "
    puts " "
    puts "Siguiente combate"
    puts " "
    puts " "
    sleep 2
    puts x.nombre+ " vs " +y.nombre
    sleep 2
    puts " "
    puts "Que el duelo comience!"
    puts " "
    sleep 1
    ganador = turno(x,y)[1]
    puts "El ganador es " + ganador.nombre.to_s
    ganador
end  
puts "Pokémon que participarán del torneo"
puts "Pokemon 1: " + @Pokemon_1.nombre
puts "Pokemon 2: " + @Pokemon_2.nombre
puts "Pokemon 3: " + @Pokemon_3.nombre
puts "Pokemon 4: " + @Pokemon_4.nombre
puts "Pokemon 5: " + @Pokemon_5.nombre
puts "Pokemon 6: " + @Pokemon_6.nombre
puts "Pokemon 7: " + @Pokemon_7.nombre
puts "Pokemon 8: " + @Pokemon_8.nombre
sleep 10
def campeonato(a,b,c,d,e,f,g,h)
    ronda1 = []
    ronda2 = []
    ronda3 = []
    n = [a,b,c,d,e,f,g,h]
    n << "Dummy" if n.size.odd?
    fixed_name = n.shuffle!.pop
    
    1.times do |i|
        two_rows = [[fixed_name]+n[0..n.size/2-1], n[n.size/2..-1].reverse]
        pairs = two_rows.transpose.shuffle 
        ronda1.push(pairs)
    end
    puts " "
    puts "RONDA 1"
    puts " "
    puts " "
    n = []
    n.push(combate(ronda1[0][0][0],ronda1[0][0][1]))
    sleep 2
    n.push(combate(ronda1[0][1][0],ronda1[0][1][1]))
    sleep 2
    n.push(combate(ronda1[0][2][0],ronda1[0][2][1]))
    sleep 2
    n.push(combate(ronda1[0][3][0],ronda1[0][3][1]))
    sleep 2
    puts " "
    puts "RONDA 2"
    puts " "
    puts " "

    final = []
    final.push(combate(n[0],n[2]))
    sleep 2
    final.push(combate(n[3],n[1]))
    sleep 2
    
    puts " "
    puts "RONDA 3"
    puts " "
    puts " "
    campeon = (combate(final[0],final[1]))
    puts " "
    puts " "
    puts " "
    sleep 2
    puts "El campeon de nuestro torneo es " + campeon.nombre
end
campeonato(@Pokemon_1, @Pokemon_2, @Pokemon_3, @Pokemon_4, @Pokemon_5, @Pokemon_6, @Pokemon_7, @Pokemon_8)