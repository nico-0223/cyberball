"""

 1. Imposta 'deviceDescription' per aprire il dispositivo USB-4750.
 2. Imposta 'profilePath' per leggere la configurazione del dispositivo  USB-4750.xml.
 3. Imposta 'startPort' nel nostro caso il DI e' il port 0.
 4. Imposta 'portCount' ne leggiamo solo uno.

 """

from Automation.BDaq import *
from Automation.BDaq.InstantDiCtrl import InstantDiCtrl
from Automation.BDaq.BDaqApi import AdxEnumToString, BioFailed

deviceDescription = "USB-4750,BID#0"  # Descrizione e Numero del dispositivo
profilePath = "USB-4750.xml"          # Profilo (configurazione)
startPort = 0                         # Il port 0 corrisponde ai digital input
portCount = 1


def LeggoPulsanti():
    ret = ErrorCode.Success

    # Creare una 'InstantDiCtrl' per la funzione DI.
    # Selezionare un dispositivo tramite numero o descrizione del dispositivo
    instantDiCtrl = InstantDiCtrl(deviceDescription)
    # Configura il dispositivo usando il file di configurazione USB-4750.xml
    instantDiCtrl.loadProfile = profilePath

    # Leggere i valori di input digitali
    ret, data = instantDiCtrl.readAny(startPort, portCount)

    # Se si verifica un errore durante l'esecuzione, il codice di errore viene visualizzato
    if BioFailed(ret):
        enumStr = AdxEnumToString("ErrorCode", ret.value, 256)
        print("Errore: %#x. [%s]" % (ret.value, enumStr))
        return 0

                        # Elaboriamo i valori letti
    giocatore1Destra   = bool(data[0] & int("00000001", 2))       # Il bit0 corrisponde alla lettura del DI0
    giocatore1Sinistra = bool((data[0] & int("00000010", 2)) >> 1) # Il bit1 corrisponde alla lettura del DI1
    giocatore2Destra   = bool((data[0] & int("00000100", 2)) >> 2) # Il bit2 corrisponde alla lettura del DI2
    giocatore2Sinistra = bool((data[0] & int("00001000", 2)) >> 3) # Il bit3 corrisponde alla lettura del DI3
    giocatore4Destra   = bool((data[0] & int("00010000", 2)) >> 4) # Il bit4 corrisponde alla lettura del DI4
    giocatore4Sinistra = bool((data[0] & int("00100000", 2)) >> 5) # Il bit5 corrisponde alla lettura del DI5
    giocatore3Destra   = bool((data[0] & int("01000000", 2)) >> 6) # Il bit4 corrisponde alla lettura del DI4
    giocatore3Sinistra = bool((data[0] & int("10000000", 2)) >> 7) 
    
    # Stampa i valori letti
    # Chiudere il dispositivo e rilasciare tutte le risorse assegnate
    instantDiCtrl.dispose()
            
    return {"G1D": giocatore1Destra, "G1S" : giocatore1Sinistra,
            "G2D": giocatore2Destra, "G2S" : giocatore2Sinistra,
            "G3D": giocatore3Destra, "G3S" : giocatore3Sinistra,
            }
                        
       