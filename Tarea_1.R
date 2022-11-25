library("readxl")
# X e Y corresponden a la variable dependiente e independiente
# W corresponde a el error estimado
#
datos <- read_excel("/home/felipe/Descargas/Datos #1.xlsx")
summary(datos)
X <- as.matrix(datos %>% transmute (c = 1, r_us, r_ch, cobre, petroleo, broad_dollar))
Y <- as.matrix(datos %>% transmute (tdc))
B = solve(t(X)%*%X)%*%(t(X)%*%Y)
Y_ = B[0]

B[1]*X[,2]
