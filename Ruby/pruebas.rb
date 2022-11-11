
#for i in competidor
#    puts "______________"
#    puts " "
#    puts i["name"]
#    puts " "
#    puts "Tipo(s)"
#    puts i["types"]
#    puts " "
#    puts "Movimientos"
#    puts i["mov_usados"]
#    puts "______________"    
#end
["1","2","3"].each do [letter]
    define_method letter.to_sym do
        hola+"#{letter}" = puts "impresión de #{letter}" 
    end
end