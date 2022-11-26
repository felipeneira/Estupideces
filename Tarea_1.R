library("readxl")
library("dplyr")
library("lmtest")
# X e Y corresponden a la variable dependiente e independiente
# W corresponde a el error estimado
#
datos <- read_excel("C:/Users/fneir/Downloads/Datos #1.xlsx")
X <- as.matrix(datos %>% transmute (c = 1, r_us, r_ch, cobre, petroleo, broad_dollar))
Y <- as.matrix(datos %>% transmute (tdc))
B <- solve(t(X)%*%X)%*%(t(X)%*%Y)
e <- as.matrix(Y-B[1]-B[2]*X[,2]-B[3]*X[,3]-B[4]*X[,4]-B[5]*X[,5]-B[6]*X[,6])
t <- length(datos$r_us)
sigma2 = (t(e)%*%e)/(t-5-1)
MV <- (-t/2*log(2*3.14*sigma2)-(1/2*sigma2)*sum(e^2))*(-1)

prueba <- lm(data = datos, tdc ~ r_us+ r_ch + cobre + petroleo + broad_dollar)
bptest(prueba)

