import sys
from subprocess import check_output

argv = sys.argv


try:
    if argv[1] == 'walk':
        print check_output(["snmpwalk", "-m", "ANDRE-GLOBAL-REG", "-c", "public", "localhost", ".1",])
    elif argv[1] == 'get':
        print check_output(["snmpget", "-c", "public", "localhost", "ANDRE-GLOBAL-REG::" + argv[2] + "." + argv[3]])
    elif argv[1] == 'container_table':
        print check_output(["snmptable", "-m", "ANDRE-GLOBAL-REG", "-c", "public", "localhost", "containeListTable"])
    elif argv[1] == 'reboot_containers':
        print check_output(["snmpset", "-m", "ANDRE-GLOBAL-REG", "-c", "private", "localhost", "dockerDaemonRestart.0", "i", "1"])
    else:
        print("Comandos\n" +
              "manager.py walk: Mostra todas as oids\n" +
              "manager.py get oid_name folha: Mostra uma oid\n" +
              "manager.py container_table: mostra informacoes da tabela de containers\n"+
              "manager.py reboot_containers: reinicia todos os containers")
except:
    print("Comandos\n" +
          "manager.py walk: Mostra todas as oids\n" +
          "manager.py get oid_name folha: Mostra uma oid\n" +
          "manager.py container_table: mostra informacoes da tabela de containers\n"+
          "manager.py reboot_containers: reinicia todos os containers")