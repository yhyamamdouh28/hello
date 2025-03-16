# $language = "Python3"
# $interface = "1.0"


import sys
import time
import datetime
import os
import csv
import webbrowser
import random
import re
import math
import string
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

################################################### Ahmed Elaraby ####################################################
######################################################################################################################


#######################################################################################################    
########################################### ETISALAT ##################################################
#######################################################################################################

def ETISALAT(user,pass1,link,AggRouter,InterRouter,Port1,Port2):
	crt.Screen.Send("show interfaces descriptions | match " + link + ".2300\r")
	crt.Screen.WaitForString("EG>")

	StatusRows = []
	PortRow = crt.Screen.CurrentRow - 1
	readPortRow1 = crt.Screen.Get(PortRow, 1,PortRow,200).strip()
	StatusRows.append(readPortRow1)

	while readPortRow1.endswith("2300") == False:
		PortRow = PortRow - 1
		readPortRow1 = crt.Screen.Get(PortRow, 1,PortRow,400).strip()
		StatusRows.append(readPortRow1)

	for i in range (0, len(StatusRows)):
		if StatusRows[i].startswith(link):
			readPortRow = StatusRows[i]

	if "up    down" in readPortRow :
		#crt.Dialog.MessageBox("up    down")
		crt.Screen.Send("clear vpls mac-move-action interface " + link + ".2300\r")
		crt.Dialog.MessageBox("check now as mac-move-action cleared")
		return 0
	if "down  up" in readPortRow :
		crt.Dialog.MessageBox("check port is disabled")
		return 0

	if "up    up" in readPortRow or "up    up" in readPortRow1 :
		#crt.Dialog.MessageBox("up    up")
		crt.Screen.Send("show configuration interfaces " + link + ".2300 | display set\r")
		crt.Screen.WaitForString("EG>")

		Rows = []
		confRow = crt.Screen.CurrentRow - 1
		readconfRow = crt.Screen.Get(confRow, 1,confRow,400).strip()
		Rows.append(readconfRow)

		while readconfRow.endswith("display set") == False:
			confRow = confRow - 1
			readconfRow = crt.Screen.Get(confRow, 1,confRow,400).strip()
			Rows.append(readconfRow)

		crt.Screen.Send("show configuration routing-instances ETISALAT-VPLS-BITSTREAM interface " + link + ".2300 | display set\r")
		crt.Screen.WaitForString("EG>")

		confRow2 = crt.Screen.CurrentRow - 1
		readconfRow2 = crt.Screen.Get(confRow2, 1,confRow2,400).strip()
		Rows.append(readconfRow2)

		while readconfRow2.endswith("display set") == False:
			confRow2 = confRow2 - 1
			readconfRow2 = crt.Screen.Get(confRow2, 1,confRow2,400).strip()
			Rows.append(readconfRow2)


		confRow1 = "set interfaces " + link + " unit 2300 encapsulation vlan-vpls"
		confRow2 = "set interfaces " + link + " unit 2300 vlan-id-range 2300-2549"
		confRow3 = "set routing-instances ETISALAT-VPLS-BITSTREAM interface " + link + ".2300"
		confRow = [confRow1,confRow2,confRow3]
		cRow = [0,0,0]
		for i in range (0, len(Rows)):
			if Rows[i] == confRow[0]:
				cRow[0] = 1
			if Rows[i] == confRow[1]:
				cRow[1] = 1
			if Rows[i] == confRow[2]:
				cRow[2] = 1

		cRowPr1 = "-"
		for i in range (0, len(cRow)):
			if cRow[i] == 0:
				cRowPr1 = cRowPr1 + confRow[i] + "\r"
		#crt.Dialog.MessageBox(cRowPr)
		cRowPr = "- NO Missing configuration" if cRowPr1 == "-" else cRowPr1


		if AggRouter == InterRouter :

			if Port2 != "@" :
				crt.Screen.Send("show interfaces " + Port1 + " terse\r")
				#crt.Screen.WaitForString("--> ")
				WaPo = crt.Screen.WaitForStrings(['--> ','vpls','EG>'],5)
				if WaPo == 1:
					Port1 = crt.Screen.ReadString(".")
					GetINTPort = 0
				if WaPo == 2:
					GetINTPort = 1
				if WaPo == 3:
					crt.Screen.Send("\r")
					GetINTPort = 1
				crt.Screen.WaitForString("EG>")

			crt.Screen.Send('show configuration routing-instances ETISALAT-VPLS-BITSTREAM | except "ETISALAT-VPLS-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			VPLSRows = []
			VconfRow = crt.Screen.CurrentRow - 1
			readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
			VPLSRows.append(readVconfRow)

			while readVconfRow.endswith("display set") == False:
				VconfRow = VconfRow - 1
				readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
				VPLSRows.append(readVconfRow)

			VconfRow1 = "set routing-instances ETISALAT-VPLS-BITSTREAM protocols vpls enable-mac-move-action"
			VconfRow2 = "set routing-instances ETISALAT-VPLS-BITSTREAM protocols vpls mac-table-size 2000"
			VconfRow3 = "set routing-instances ETISALAT-VPLS-BITSTREAM protocols vpls no-tunnel-services"
			VconfRow4 = "set routing-instances ETISALAT-VPLS-BITSTREAM protocols vpls vpls-id 2300"
			VconfRow5 = "set routing-instances ETISALAT-VPLS-BITSTREAM instance-type vpls"
			VconfRow6 = "set routing-instances ETISALAT-VPLS-BITSTREAM vlan-id all"
			VconfRow7 = "set routing-instances ETISALAT-VPLS-BITSTREAM protocols vpls interface"

			VconfRow = [VconfRow1 , VconfRow2 , VconfRow3 , VconfRow4 , VconfRow5 , VconfRow6 , VconfRow7]

			VcRow = [0,0,0,0,0,0,0]
			for i in range (0, len(VPLSRows)):
				if VPLSRows[i] == VconfRow[0]:
					VcRow[0] = 1
				if VPLSRows[i] == VconfRow[1]:
					VcRow[1] = 1
				if VPLSRows[i] == VconfRow[2]:
					VcRow[2] = 1
				if VPLSRows[i] == VconfRow[3]:
					VcRow[3] = 1
				if VPLSRows[i] == VconfRow[4]:
					VcRow[4] = 1
				if VPLSRows[i] == VconfRow[5]:
					VcRow[5] = 1
				if VPLSRows[i].startswith(VconfRow[6]) == True:
					VcRow[6] = 1
					interPort0 = VPLSRows[i].split("interface ")
					interPort1 = interPort0[1].split(".")
					interPort = interPort1[0]
					#crt.Dialog.MessageBox(str(interPort))
					if Port1 != interPort:
						Port1 = interPort
					GetINTPort = 0

			VcRowPr1 = "-"
			for i in range (0, len(VcRow)):
				if VcRow[i] == 0:
					VcRowPr1 = VcRowPr1 + VconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			VcRowPr = "- NO Missing configuration" if VcRowPr1 == "-" else VcRowPr1

			if GetINTPort == 1:
				crt.Screen.Send("show vpls mac-table instance ETISALAT-VPLS-BITSTREAM | no-more\r")
				crt.Screen.WaitForString("Routing instance : ETISALAT-VPLS-BITSTREAM")
				readINTPortST = crt.Screen.ReadString("MAC flags")
				readINTPortrows = readINTPortST.splitlines()
				#readINTPortrows = [item.strip() for item in readINTPortrows]
				for i in range (0, len(readINTPortrows)):
					if ".2300" in readINTPortrows[i]:
						readINTPortrow1 = readINTPortrows[i]
						readINTPortrow2 = readINTPortrow1.split("D")
						readINTPortrow = readINTPortrow2[1].strip()
						Port12 = readINTPortrow.split(".")
						Port1 = Port12[0]
				crt.Screen.WaitForString("EG>")

			crt.Screen.Send("show configuration interfaces " + Port1 + ".2300 | display set\r")
			crt.Screen.WaitForString("EG>")

			IRows = []
			IconfRow = crt.Screen.CurrentRow - 1
			readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
			IRows.append(readIconfRow)

			while readIconfRow.endswith("display set") == False:
				IconfRow = IconfRow - 1
				readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
				IRows.append(readIconfRow)

			crt.Screen.Send("show configuration routing-instances ETISALAT-VPLS-BITSTREAM interface " + Port1 + ".2300 | display set\r")
			crt.Screen.WaitForString("EG>")

			IconfRow2 = crt.Screen.CurrentRow - 1
			readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
			IRows.append(readIconfRow2)

			while readIconfRow2.endswith("display set") == False:
				IconfRow2 = IconfRow2 - 1
				readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
				IRows.append(readIconfRow2)

			IconfRow1 = "set interfaces " + Port1 + " unit 2300 encapsulation vlan-vpls"
			IconfRow2 = "set interfaces " + Port1 + " unit 2300 vlan-id-range 2300-2549"
			IconfRow3 = "set routing-instances ETISALAT-VPLS-BITSTREAM interface " + Port1 + ".2300"
			IconfRow = [IconfRow1,IconfRow2,IconfRow3]
			IcRow = [0,0,0]
			for i in range (0, len(IRows)):
				if IRows[i] == IconfRow[0]:
					IcRow[0] = 1
				if IRows[i] == IconfRow[1]:
					IcRow[1] = 1
				if IRows[i] == IconfRow[2]:
					IcRow[2] = 1

			IcRowPr1 = "-"
			for i in range (0, len(IcRow)):
				if IcRow[i] == 0:
					IcRowPr1 = IcRowPr1 + IconfRow[i] + "\r"
			#crt.Dialog.MessageBox(cRowPr)
			IcRowPr = "- NO Missing configuration" if IcRowPr1 == "-" else IcRowPr1


			vlanNums = crt.Dialog.Prompt("Please Enter affected VLANs seperating with space :","Ahmed Elaraby")
			VLANs = vlanNums.split()
			MACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 2300 and int(VlanNum) <= 2549:
						
					crt.Screen.Send("show vpls mac-table instance ETISALAT-VPLS-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if Port1 + ".2300" in VLANRows[j]:
							MACs.append("There is MAC from ETISALAT side for VLAN " + VlanNum)

						if link +".2300" in VLANRows[j]:
							MACs.append("There is MAC from Customer side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					MACs.append(addVlan)

			MACsPr1 = "-"
			MACs = list(dict.fromkeys(MACs))
			for i in range (0, len(MACs)):
				MACsPr1 = MACsPr1 + MACs[i] + "\r"

			MACsPr = "- NO MACs received from both side" if MACsPr1 == "-" else MACsPr1

			crt.Screen.Send("show interfaces " + Port1 + " | no-more\r")
			crt.Screen.WaitForString("Physical link is")
			InterPortStatus = str(crt.Screen.ReadString("Interface index")).strip()

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match last \r")
			crt.Screen.WaitForString("(")
			InterPortLastFlap = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match rate \r")
			crt.Screen.WaitForString("Input rate")
			InterPortInputRate = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("Output rate")
			InterPortOutputRate = crt.Screen.ReadString(")")




			crt.Dialog.MessageBox("            *****ETISALAT-VPLS-BITSTREAM*****\r\r* MX Router : " + AggRouter + "\r\r* MX Port : " + link + "\r\r* Status : UP\r\r* Checking MX Port configuration :\r" + cRowPr +  "\r\r* Checking VPLS configuration :\r" + VcRowPr + "\r\r* Interconnection Router : "+ InterRouter + "\r\r* Interconnection Port : " + Port1 + "\r\r* Status : " + InterPortStatus + "\r\r* Last Flap : " + InterPortLastFlap + "\r\r* Input Rate" + InterPortInputRate + ")\r* Output Rate" + InterPortOutputRate + ")\r\r* Checking Interconnection Port configuration :\r" + IcRowPr +  "\r\r* MACs : \r" + MACsPr  ,"Ahmed Elaraby", BUTTON_CANCEL + ICON_INFO)



		if AggRouter != InterRouter :
			#crt.Dialog.MessageBox("AggRouter != InterRouter")
			crt.Screen.Send('show configuration routing-instances ETISALAT-VPLS-BITSTREAM | except "ETISALAT-VPLS-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			VPLSRows = []
			VconfRow = crt.Screen.CurrentRow - 1
			readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
			VPLSRows.append(readVconfRow)

			while readVconfRow.endswith("display set") == False:
				VconfRow = VconfRow - 1
				readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
				VPLSRows.append(readVconfRow)

			VconfRow1 = "set routing-instances ETISALAT-VPLS-BITSTREAM protocols vpls enable-mac-move-action"
			VconfRow2 = "set routing-instances ETISALAT-VPLS-BITSTREAM protocols vpls mac-table-size 2000"
			VconfRow3 = "set routing-instances ETISALAT-VPLS-BITSTREAM protocols vpls no-tunnel-services"
			VconfRow4 = "set routing-instances ETISALAT-VPLS-BITSTREAM protocols vpls vpls-id 2300"
			VconfRow5 = "set routing-instances ETISALAT-VPLS-BITSTREAM instance-type vpls"
			VconfRow6 = "set routing-instances ETISALAT-VPLS-BITSTREAM vlan-id all"
			VconfRow7 = "set routing-instances ETISALAT-VPLS-BITSTREAM protocols vpls neighbor"

			VconfRow = [VconfRow1 , VconfRow2 , VconfRow3 , VconfRow4 , VconfRow5 , VconfRow6 , VconfRow7]

			VcRow = [0,0,0,0,0,0,0]
			neigIP = "@"
			for i in range (0, len(VPLSRows)):
				if VPLSRows[i] == VconfRow[0]:
					VcRow[0] = 1
				if VPLSRows[i] == VconfRow[1]:
					VcRow[1] = 1
				if VPLSRows[i] == VconfRow[2]:
					VcRow[2] = 1
				if VPLSRows[i] == VconfRow[3]:
					VcRow[3] = 1
				if VPLSRows[i] == VconfRow[4]:
					VcRow[4] = 1
				if VPLSRows[i] == VconfRow[5]:
					VcRow[5] = 1
				if VPLSRows[i].startswith(VconfRow[6]) == True:
					VcRow[6] = 1
					neigIP0 = VPLSRows[i].split("neighbor ")
					neigIP1 = neigIP0[1].split(" ")
					neigIP = neigIP1[0]

			"""
			if neigIP == "@":

				data =[]
				FileName = "Devices.csv"
				try:
					with open(os.path.join(os.path.dirname(__file__), FileName), mode='r') as csvfile:
						reader = csv.reader(csvfile)
						for row in reader:
							data.append(row)
				except EnvironmentError:
					crt.Dialog.MessageBox("Sorry Can't Open File! Please Change Files and Script Location!","Ahmed Elaraby")
					return 0

				TARGETCICol = [x[11] for x in data]
				if InterRouter in TARGETCICol:
					for x in range(0,len(data)):
						if InterRouter == data[x][11]:
							neigIP = data[x][5]
			"""


			VcRowPr1 = "-"
			for i in range (0, len(VcRow)):
				if VcRow[i] == 0:
					VcRowPr1 = VcRowPr1 + VconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			VcRowPr = "- NO Missing configuration" if VcRowPr1 == "-" else VcRowPr1

			crt.Screen.Send("show vpls connections instance ETISALAT-VPLS-BITSTREAM | no-more\r")
			crt.Screen.WaitForString("EG>")

			NeigRows = []
			NeigRow = crt.Screen.CurrentRow - 1
			readNeigRow = crt.Screen.Get(NeigRow, 1,NeigRow,400).strip()
			NeigRows.append(readNeigRow)

			while readNeigRow.endswith("ETISALAT-VPLS-BITSTREAM") == False:
				NeigRow = NeigRow - 1
				readNeigRow = crt.Screen.Get(NeigRow, 1,NeigRow,400).strip()
				NeigRows.append(readNeigRow)

			for i in range (0, len(NeigRows)):
				if NeigRows[i].startswith(neigIP):
					vplsconnrow = NeigRows[i]
					#crt.Dialog.MessageBox(str(vplsconnrow))


			vlanNums = crt.Dialog.Prompt("Please Enter affected VLANs seperating with space :","Ahmed Elaraby")
			VLANs = vlanNums.split()
			MXMACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 2300 and int(VlanNum) <= 2549:
						
					crt.Screen.Send("show vpls mac-table instance ETISALAT-VPLS-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if "lsi" in VLANRows[j]:
							MXMACs.append("There is MAC from Interconnection side [ETISALAT] for VLAN " + VlanNum)

						if link +".2300" in VLANRows[j]:
							MXMACs.append("There is MAC from Customer side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					MXMACs.append(addVlan)

			MACsPr1 = "-"
			MXMACs = list(dict.fromkeys(MXMACs))
			for i in range (0, len(MXMACs)):
				MACsPr1 = MACsPr1 + MXMACs[i] + "\r"

			MACsPr = "- NO MACs received from both side" if MACsPr1 == "-" else MACsPr1

			crt.Screen.Send("show interfaces lo0.0\r")
			crt.Screen.WaitForString("Local: ")
			MXRouterIP = crt.Screen.ReadString("\r").strip()
			#crt.Dialog.MessageBox(MXRouterIP)

			crt.Screen.Send("quit\r")
			crt.Screen.WaitForString("~]$")
			if neigIP == "@":
				crt.Screen.Send("alias " + InterRouter + "\r")
				crt.Screen.WaitForString("telnet")
				neigIP = crt.Screen.ReadString("'").strip()
				crt.Screen.WaitForString("~]$")

			crt.Screen.Send("telnet " + neigIP + "\r")
			crt.Screen.WaitForString("login:")
			crt.Screen.Send(user+"\r")
			crt.Screen.WaitForString("Password:")
			crt.Screen.Send(pass1+"\r")
			crt.Screen.WaitForString("EG>")

			if Port2 != "@" :
				crt.Screen.Send("show interfaces " + Port1 + " terse\r")
				#crt.Screen.WaitForString("--> ")
				WaPo = crt.Screen.WaitForStrings(['--> ','vpls','EG>'],5)
				if WaPo == 1:
					Port1 = crt.Screen.ReadString(".")
					GetINTPort = 0
				if WaPo == 2:
					GetINTPort = 1
				if WaPo == 3:
					crt.Screen.Send("\r")
					GetINTPort = 1
				crt.Screen.WaitForString("EG>")

			

			crt.Screen.Send('show configuration routing-instances ETISALAT-VPLS-BITSTREAM | except "ETISALAT-VPLS-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			IVPLSRows = []
			IVconfRow = crt.Screen.CurrentRow - 1
			readIVconfRow = crt.Screen.Get(IVconfRow, 1,IVconfRow,400).strip()
			IVPLSRows.append(readIVconfRow)

			while readIVconfRow.endswith("display set") == False:
				IVconfRow = IVconfRow - 1
				readIVconfRow = crt.Screen.Get(IVconfRow, 1,IVconfRow,400).strip()
				IVPLSRows.append(readIVconfRow)

			IVconfRow1 = "set routing-instances ETISALAT-VPLS-BITSTREAM protocols vpls enable-mac-move-action"
			IVconfRow2 = "set routing-instances ETISALAT-VPLS-BITSTREAM protocols vpls mac-table-size 2000"
			IVconfRow3 = "set routing-instances ETISALAT-VPLS-BITSTREAM protocols vpls no-tunnel-services"
			IVconfRow4 = "set routing-instances ETISALAT-VPLS-BITSTREAM protocols vpls vpls-id 2300"
			IVconfRow5 = "set routing-instances ETISALAT-VPLS-BITSTREAM instance-type vpls"
			IVconfRow6 = "set routing-instances ETISALAT-VPLS-BITSTREAM vlan-id all"
			IVconfRow7 = "set routing-instances ETISALAT-VPLS-BITSTREAM protocols vpls interface"

			IVconfRow = [IVconfRow1 , IVconfRow2 , IVconfRow3 , IVconfRow4 , IVconfRow5 , IVconfRow6 , IVconfRow7]

			IVcRow = [0,0,0,0,0,0,0]
			for i in range (0, len(IVPLSRows)):
				if IVPLSRows[i] == IVconfRow[0]:
					IVcRow[0] = 1
				if IVPLSRows[i] == IVconfRow[1]:
					IVcRow[1] = 1
				if IVPLSRows[i] == IVconfRow[2]:
					IVcRow[2] = 1
				if IVPLSRows[i] == IVconfRow[3]:
					IVcRow[3] = 1
				if IVPLSRows[i] == IVconfRow[4]:
					IVcRow[4] = 1
				if IVPLSRows[i] == IVconfRow[5]:
					IVcRow[5] = 1
				if IVPLSRows[i].startswith(IVconfRow[6]) == True:
					IVcRow[6] = 1
					interPort0 = IVPLSRows[i].split("interface ")
					interPort1 = interPort0[1].split(".")
					interPort = interPort1[0]
					#crt.Dialog.MessageBox(str(interPort))
					if Port1 != interPort:
						Port1 = interPort
					GetINTPort = 0

			IVcRowPr1 = "-"
			for i in range (0, len(IVcRow)):
				if IVcRow[i] == 0:
					IVcRowPr1 = IVcRowPr1 + IVconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			IVcRowPr = "- NO Missing configuration" if IVcRowPr1 == "-" else IVcRowPr1

			if GetINTPort == 1:
				crt.Screen.Send("show vpls mac-table instance ETISALAT-VPLS-BITSTREAM | no-more\r")
				crt.Screen.WaitForString("Routing instance : ETISALAT-VPLS-BITSTREAM")
				readINTPortST = crt.Screen.ReadString("MAC flags")
				readINTPortrows = readINTPortST.splitlines()
				#readINTPortrows = [item.strip() for item in readINTPortrows]
				for i in range (0, len(readINTPortrows)):
					if ".2300" in readINTPortrows[i]:
						readINTPortrow1 = readINTPortrows[i]
						readINTPortrow2 = readINTPortrow1.split("D")
						readINTPortrow = readINTPortrow2[1].strip()
						Port12 = readINTPortrow.split(".")
						Port1 = Port12[0]
				crt.Screen.WaitForString("EG>")


			crt.Screen.Send("show configuration interfaces " + Port1 + ".2300 | display set\r")
			crt.Screen.WaitForString("EG>")

			IRows = []
			IconfRow = crt.Screen.CurrentRow - 1
			readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
			IRows.append(readIconfRow)

			while readIconfRow.endswith("display set") == False:
				IconfRow = IconfRow - 1
				readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
				IRows.append(readIconfRow)

			crt.Screen.Send("show configuration routing-instances ETISALAT-VPLS-BITSTREAM interface " + Port1 + ".2300 | display set\r")
			crt.Screen.WaitForString("EG>")

			IconfRow2 = crt.Screen.CurrentRow - 1
			readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
			IRows.append(readIconfRow2)

			while readIconfRow2.endswith("display set") == False:
				IconfRow2 = IconfRow2 - 1
				readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
				IRows.append(readIconfRow2)

			IconfRow1 = "set interfaces " + Port1 + " unit 2300 encapsulation vlan-vpls"
			IconfRow2 = "set interfaces " + Port1 + " unit 2300 vlan-id-range 2300-2549"
			IconfRow3 = "set routing-instances ETISALAT-VPLS-BITSTREAM interface " + Port1 + ".2300"
			IconfRow = [IconfRow1,IconfRow2,IconfRow3]
			IcRow = [0,0,0]
			for i in range (0, len(IRows)):
				if IRows[i] == IconfRow[0]:
					IcRow[0] = 1
				if IRows[i] == IconfRow[1]:
					IcRow[1] = 1
				if IRows[i] == IconfRow[2]:
					IcRow[2] = 1

			IcRowPr1 = "-"
			for i in range (0, len(IcRow)):
				if IcRow[i] == 0:
					IcRowPr1 = IcRowPr1 + IconfRow[i] + "\r"
			#crt.Dialog.MessageBox(cRowPr)
			IcRowPr = "- NO Missing configuration" if IcRowPr1 == "-" else IcRowPr1

			"""
			crt.Screen.Send("show vpls connections instance ETISALAT-VPLS-BITSTREAM | no-more\r")
			crt.Screen.WaitForString("EG>")

			INeigRows = []
			INeigRow = crt.Screen.CurrentRow - 1
			readINeigRow = crt.Screen.Get(INeigRow, 1,INeigRow,400).strip()
			INeigRows.append(readINeigRow)

			while readINeigRow.endswith("ETISALAT-VPLS-BITSTREAM") == False:
				INeigRow = INeigRow - 1
				readINeigRow = crt.Screen.Get(INeigRow, 1,INeigRow,400).strip()
				INeigRows.append(readINeigRow)

			for i in range (0, len(INeigRows)):
				if INeigRows[i].startswith(MXRouterIP):
					Ivplsconnrow = INeigRows[i]
					#crt.Dialog.MessageBox(str(vplsconnrow))
			"""

			crt.Screen.Send("show vpls connections instance ETISALAT-VPLS-BITSTREAM | no-more\r")
			crt.Screen.WaitForString("ETISALAT-VPLS-BITSTREAM")
			OVBRead = crt.Screen.ReadString("EG>")

			INeigRows = OVBRead.splitlines()
			INeigRows = [item.strip() for item in INeigRows]

			for i in range (0, len(INeigRows)):
				if MXRouterIP + "(" in INeigRows[i]:
					Ivplsconnrow = INeigRows[i]
					#crt.Dialog.MessageBox(str(vplsconnrow))

			INTMACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 2300 and int(VlanNum) <= 2549:
						
					crt.Screen.Send("show vpls mac-table instance ETISALAT-VPLS-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if "lsi" in VLANRows[j]:
							INTMACs.append("There is MAC from MX Router side [customer] for VLAN " + VlanNum)

						if Port1 +".2300" in VLANRows[j]:
							INTMACs.append("There is MAC from ETISALAT side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					INTMACs.append(addVlan)

			IMACsPr1 = "-"
			INTMACs = list(dict.fromkeys(INTMACs))
			for i in range (0, len(INTMACs)):
				IMACsPr1 = IMACsPr1 + INTMACs[i] + "\r"

			IMACsPr = "- NO MACs received from both side" if IMACsPr1 == "-" else IMACsPr1

			crt.Screen.Send("show interfaces " + Port1 + " | no-more\r")
			crt.Screen.WaitForString("Physical link is")
			InterPortStatus = str(crt.Screen.ReadString("Interface index")).strip()

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match last \r")
			crt.Screen.WaitForString("(")
			InterPortLastFlap = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match rate \r")
			crt.Screen.WaitForString("Input rate")
			InterPortInputRate = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("Output rate")
			InterPortOutputRate = crt.Screen.ReadString(")")


			crt.Dialog.MessageBox("            *****ETISALAT-VPLS-BITSTREAM*****\r\r* MX Router : " + AggRouter + "\r\r* MX Port : " + link + "\r\r* Status : UP\r\r* Checking MX Port configuration :\r" + cRowPr + "\r\r* Checking MX VPLS configuration :\r" + VcRowPr + "\r\r* vpls connections Status on MX :\r" + vplsconnrow + "\r\r* MACs on MX : \r" + MACsPr + "\r\r* Interconnection Router : "+ InterRouter + "\r\r* Interconnection Port : " + Port1 + "\r\r* Status : " + InterPortStatus + "\r\r* Last Flap : " + InterPortLastFlap + "\r\r* Input Rate" + InterPortInputRate + ")\r* Output Rate" + InterPortOutputRate + ")\r\r* Checking Interconnection Port configuration :\r" + IcRowPr + "\r\r* Checking Interconnection VPLS configuration :\r" + IVcRowPr + "\r\r* vpls connections Status on Interconnection :\r" + Ivplsconnrow + "\r\r* MACs on Interconnection : \r" + IMACsPr ,"Ahmed Elaraby", BUTTON_CANCEL + ICON_INFO)


#######################################################################################################    
########################################### ETISALAT MOBILE ###########################################
#######################################################################################################

def ETISALATMOB(user,pass1,link,AggRouter,InterRouter,Port1,Port2):
	crt.Screen.Send("show interfaces descriptions | match " + link + ".1751\r")
	crt.Screen.WaitForString("EG>")

	StatusRows = []
	PortRow = crt.Screen.CurrentRow - 1
	readPortRow1 = crt.Screen.Get(PortRow, 1,PortRow,200).strip()
	StatusRows.append(readPortRow1)

	while readPortRow1.endswith("1751") == False:
		PortRow = PortRow - 1
		readPortRow1 = crt.Screen.Get(PortRow, 1,PortRow,400).strip()
		StatusRows.append(readPortRow1)

	for i in range (0, len(StatusRows)):
		if StatusRows[i].startswith(link):
			readPortRow = StatusRows[i]

	if "up    down" in readPortRow :
		#crt.Dialog.MessageBox("up    down")
		crt.Screen.Send("clear vpls mac-move-action interface " + link + ".1751\r")
		crt.Dialog.MessageBox("check now as mac-move-action cleared")
		return 0
	if "down  up" in readPortRow :
		crt.Dialog.MessageBox("check port is disabled")
		return 0

	if "up    up" in readPortRow or "up    up" in readPortRow1 :
		#crt.Dialog.MessageBox("up    up")
		crt.Screen.Send("show configuration interfaces " + link + ".1751 | display set\r")
		crt.Screen.WaitForString("EG>")

		Rows = []
		confRow = crt.Screen.CurrentRow - 1
		readconfRow = crt.Screen.Get(confRow, 1,confRow,400).strip()
		Rows.append(readconfRow)

		while readconfRow.endswith("display set") == False:
			confRow = confRow - 1
			readconfRow = crt.Screen.Get(confRow, 1,confRow,400).strip()
			Rows.append(readconfRow)

		crt.Screen.Send("show configuration routing-instances ETISALAT-MOB-BITSTREAM interface " + link + ".1751 | display set\r")
		crt.Screen.WaitForString("EG>")

		confRow2 = crt.Screen.CurrentRow - 1
		readconfRow2 = crt.Screen.Get(confRow2, 1,confRow2,400).strip()
		Rows.append(readconfRow2)

		while readconfRow2.endswith("display set") == False:
			confRow2 = confRow2 - 1
			readconfRow2 = crt.Screen.Get(confRow2, 1,confRow2,400).strip()
			Rows.append(readconfRow2)


		confRow1 = "set interfaces " + link + " unit 1751 encapsulation vlan-vpls"
		confRow2 = "set interfaces " + link + " unit 1751 vlan-id-range 1751-1770"
		confRow3 = "set routing-instances ETISALAT-MOB-BITSTREAM interface " + link + ".1751"
		confRow = [confRow1,confRow2,confRow3]
		cRow = [0,0,0]
		for i in range (0, len(Rows)):
			if Rows[i] == confRow[0]:
				cRow[0] = 1
			if Rows[i] == confRow[1]:
				cRow[1] = 1
			if Rows[i] == confRow[2]:
				cRow[2] = 1

		cRowPr1 = "-"
		for i in range (0, len(cRow)):
			if cRow[i] == 0:
				cRowPr1 = cRowPr1 + confRow[i] + "\r"
		#crt.Dialog.MessageBox(cRowPr)
		cRowPr = "- NO Missing configuration" if cRowPr1 == "-" else cRowPr1


		if AggRouter == InterRouter :

			if Port2 != "@" :
				crt.Screen.Send("show interfaces " + Port1 + " terse\r")
				#crt.Screen.WaitForString("--> ")
				WaPo = crt.Screen.WaitForStrings(['--> ','vpls','EG>'],5)
				if WaPo == 1:
					Port1 = crt.Screen.ReadString(".")
					GetINTPort = 0
				if WaPo == 2:
					GetINTPort = 1
				if WaPo == 3:
					crt.Screen.Send("\r")
					GetINTPort = 1
				crt.Screen.WaitForString("EG>")

			crt.Screen.Send('show configuration routing-instances ETISALAT-MOB-BITSTREAM | except "ETISALAT-MOB-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			VPLSRows = []
			VconfRow = crt.Screen.CurrentRow - 1
			readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
			VPLSRows.append(readVconfRow)

			while readVconfRow.endswith("display set") == False:
				VconfRow = VconfRow - 1
				readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
				VPLSRows.append(readVconfRow)

			VconfRow1 = "set routing-instances ETISALAT-MOB-BITSTREAM protocols vpls enable-mac-move-action"
			VconfRow2 = "set routing-instances ETISALAT-MOB-BITSTREAM protocols vpls mac-table-size 2000"
			VconfRow3 = "set routing-instances ETISALAT-MOB-BITSTREAM protocols vpls no-tunnel-services"
			VconfRow4 = "set routing-instances ETISALAT-MOB-BITSTREAM protocols vpls vpls-id 1751"
			VconfRow5 = "set routing-instances ETISALAT-MOB-BITSTREAM instance-type vpls"
			VconfRow6 = "set routing-instances ETISALAT-MOB-BITSTREAM vlan-id all"
			VconfRow7 = "set routing-instances ETISALAT-MOB-BITSTREAM protocols vpls interface"

			VconfRow = [VconfRow1 , VconfRow2 , VconfRow3 , VconfRow4 , VconfRow5 , VconfRow6 , VconfRow7]

			VcRow = [0,0,0,0,0,0,0]
			for i in range (0, len(VPLSRows)):
				if VPLSRows[i] == VconfRow[0]:
					VcRow[0] = 1
				if VPLSRows[i] == VconfRow[1]:
					VcRow[1] = 1
				if VPLSRows[i] == VconfRow[2]:
					VcRow[2] = 1
				if VPLSRows[i] == VconfRow[3]:
					VcRow[3] = 1
				if VPLSRows[i] == VconfRow[4]:
					VcRow[4] = 1
				if VPLSRows[i] == VconfRow[5]:
					VcRow[5] = 1
				if VPLSRows[i].startswith(VconfRow[6]) == True:
					VcRow[6] = 1
					interPort0 = VPLSRows[i].split("interface ")
					interPort1 = interPort0[1].split(".")
					interPort = interPort1[0]
					#crt.Dialog.MessageBox(str(interPort))
					if Port1 != interPort:
						Port1 = interPort
					GetINTPort = 0

			VcRowPr1 = "-"
			for i in range (0, len(VcRow)):
				if VcRow[i] == 0:
					VcRowPr1 = VcRowPr1 + VconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			VcRowPr = "- NO Missing configuration" if VcRowPr1 == "-" else VcRowPr1

			if GetINTPort == 1:
				crt.Screen.Send("show vpls mac-table instance ETISALAT-MOB-BITSTREAM | no-more\r")
				crt.Screen.WaitForString("Routing instance : ETISALAT-MOB-BITSTREAM")
				readINTPortST = crt.Screen.ReadString("MAC flags")
				readINTPortrows = readINTPortST.splitlines()
				#readINTPortrows = [item.strip() for item in readINTPortrows]
				for i in range (0, len(readINTPortrows)):
					if ".1751" in readINTPortrows[i]:
						readINTPortrow1 = readINTPortrows[i]
						readINTPortrow2 = readINTPortrow1.split("D")
						readINTPortrow = readINTPortrow2[1].strip()
						Port12 = readINTPortrow.split(".")
						Port1 = Port12[0]
				crt.Screen.WaitForString("EG>")

			crt.Screen.Send("show configuration interfaces " + Port1 + ".1751 | display set\r")
			crt.Screen.WaitForString("EG>")

			IRows = []
			IconfRow = crt.Screen.CurrentRow - 1
			readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
			IRows.append(readIconfRow)

			while readIconfRow.endswith("display set") == False:
				IconfRow = IconfRow - 1
				readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
				IRows.append(readIconfRow)

			crt.Screen.Send("show configuration routing-instances ETISALAT-MOB-BITSTREAM interface " + Port1 + ".1751 | display set\r")
			crt.Screen.WaitForString("EG>")

			IconfRow2 = crt.Screen.CurrentRow - 1
			readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
			IRows.append(readIconfRow2)

			while readIconfRow2.endswith("display set") == False:
				IconfRow2 = IconfRow2 - 1
				readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
				IRows.append(readIconfRow2)

			IconfRow1 = "set interfaces " + Port1 + " unit 1751 encapsulation vlan-vpls"
			IconfRow2 = "set interfaces " + Port1 + " unit 1751 vlan-id-range 1751-1770"
			IconfRow3 = "set routing-instances ETISALAT-MOB-BITSTREAM interface " + Port1 + ".1751"
			IconfRow = [IconfRow1,IconfRow2,IconfRow3]
			IcRow = [0,0,0]
			for i in range (0, len(IRows)):
				if IRows[i] == IconfRow[0]:
					IcRow[0] = 1
				if IRows[i] == IconfRow[1]:
					IcRow[1] = 1
				if IRows[i] == IconfRow[2]:
					IcRow[2] = 1

			IcRowPr1 = "-"
			for i in range (0, len(IcRow)):
				if IcRow[i] == 0:
					IcRowPr1 = IcRowPr1 + IconfRow[i] + "\r"
			#crt.Dialog.MessageBox(cRowPr)
			IcRowPr = "- NO Missing configuration" if IcRowPr1 == "-" else IcRowPr1


			vlanNums = crt.Dialog.Prompt("Please Enter affected VLANs seperating with space :","Ahmed Elaraby")
			VLANs = vlanNums.split()
			MACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 1751 and int(VlanNum) <= 1770:
						
					crt.Screen.Send("show vpls mac-table instance ETISALAT-MOB-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if Port1 + ".1751" in VLANRows[j]:
							MACs.append("There is MAC from ETISALAT side for VLAN " + VlanNum)

						if link +".1751" in VLANRows[j]:
							MACs.append("There is MAC from Customer side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					MACs.append(addVlan)

			MACsPr1 = "-"
			MACs = list(dict.fromkeys(MACs))
			for i in range (0, len(MACs)):
				MACsPr1 = MACsPr1 + MACs[i] + "\r"

			MACsPr = "- NO MACs received from both side" if MACsPr1 == "-" else MACsPr1

			crt.Screen.Send("show interfaces " + Port1 + " | no-more\r")
			crt.Screen.WaitForString("Physical link is")
			InterPortStatus = str(crt.Screen.ReadString("Interface index")).strip()

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match last \r")
			crt.Screen.WaitForString("(")
			InterPortLastFlap = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match rate \r")
			crt.Screen.WaitForString("Input rate")
			InterPortInputRate = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("Output rate")
			InterPortOutputRate = crt.Screen.ReadString(")")




			crt.Dialog.MessageBox("            *****ETISALAT-MOB-BITSTREAM*****\r\r* MX Router : " + AggRouter + "\r\r* MX Port : " + link + "\r\r* Status : UP\r\r* Checking MX Port configuration :\r" + cRowPr +  "\r\r* Checking VPLS configuration :\r" + VcRowPr + "\r\r* Interconnection Router : "+ InterRouter + "\r\r* Interconnection Port : " + Port1 + "\r\r* Status : " + InterPortStatus + "\r\r* Last Flap : " + InterPortLastFlap + "\r\r* Input Rate" + InterPortInputRate + ")\r* Output Rate" + InterPortOutputRate + ")\r\r* Checking Interconnection Port configuration :\r" + IcRowPr +  "\r\r* MACs : \r" + MACsPr  ,"Ahmed Elaraby", BUTTON_CANCEL + ICON_INFO)



		if AggRouter != InterRouter :
			#crt.Dialog.MessageBox("AggRouter != InterRouter")
			crt.Screen.Send('show configuration routing-instances ETISALAT-MOB-BITSTREAM | except "ETISALAT-MOB-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			VPLSRows = []
			VconfRow = crt.Screen.CurrentRow - 1
			readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
			VPLSRows.append(readVconfRow)

			while readVconfRow.endswith("display set") == False:
				VconfRow = VconfRow - 1
				readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
				VPLSRows.append(readVconfRow)

			VconfRow1 = "set routing-instances ETISALAT-MOB-BITSTREAM protocols vpls enable-mac-move-action"
			VconfRow2 = "set routing-instances ETISALAT-MOB-BITSTREAM protocols vpls mac-table-size 2000"
			VconfRow3 = "set routing-instances ETISALAT-MOB-BITSTREAM protocols vpls no-tunnel-services"
			VconfRow4 = "set routing-instances ETISALAT-MOB-BITSTREAM protocols vpls vpls-id 1751"
			VconfRow5 = "set routing-instances ETISALAT-MOB-BITSTREAM instance-type vpls"
			VconfRow6 = "set routing-instances ETISALAT-MOB-BITSTREAM vlan-id all"
			VconfRow7 = "set routing-instances ETISALAT-MOB-BITSTREAM protocols vpls neighbor"

			VconfRow = [VconfRow1 , VconfRow2 , VconfRow3 , VconfRow4 , VconfRow5 , VconfRow6 , VconfRow7]

			VcRow = [0,0,0,0,0,0,0]
			neigIP = "@"
			for i in range (0, len(VPLSRows)):
				if VPLSRows[i] == VconfRow[0]:
					VcRow[0] = 1
				if VPLSRows[i] == VconfRow[1]:
					VcRow[1] = 1
				if VPLSRows[i] == VconfRow[2]:
					VcRow[2] = 1
				if VPLSRows[i] == VconfRow[3]:
					VcRow[3] = 1
				if VPLSRows[i] == VconfRow[4]:
					VcRow[4] = 1
				if VPLSRows[i] == VconfRow[5]:
					VcRow[5] = 1
				if VPLSRows[i].startswith(VconfRow[6]) == True:
					VcRow[6] = 1
					neigIP0 = VPLSRows[i].split("neighbor ")
					neigIP1 = neigIP0[1].split(" ")
					neigIP = neigIP1[0]

			"""
			if neigIP == "@":

				data =[]
				FileName = "Devices.csv"
				try:
					with open(os.path.join(os.path.dirname(__file__), FileName), mode='r') as csvfile:
						reader = csv.reader(csvfile)
						for row in reader:
							data.append(row)
				except EnvironmentError:
					crt.Dialog.MessageBox("Sorry Can't Open File! Please Change Files and Script Location!","Ahmed Elaraby")
					return 0

				TARGETCICol = [x[11] for x in data]
				if InterRouter in TARGETCICol:
					for x in range(0,len(data)):
						if InterRouter == data[x][11]:
							neigIP = data[x][5]
			"""


			VcRowPr1 = "-"
			for i in range (0, len(VcRow)):
				if VcRow[i] == 0:
					VcRowPr1 = VcRowPr1 + VconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			VcRowPr = "- NO Missing configuration" if VcRowPr1 == "-" else VcRowPr1

			crt.Screen.Send("show vpls connections instance ETISALAT-MOB-BITSTREAM | no-more\r")
			crt.Screen.WaitForString("EG>")

			NeigRows = []
			NeigRow = crt.Screen.CurrentRow - 1
			readNeigRow = crt.Screen.Get(NeigRow, 1,NeigRow,400).strip()
			NeigRows.append(readNeigRow)

			while readNeigRow.endswith("ETISALAT-MOB-BITSTREAM") == False:
				NeigRow = NeigRow - 1
				readNeigRow = crt.Screen.Get(NeigRow, 1,NeigRow,400).strip()
				NeigRows.append(readNeigRow)

			for i in range (0, len(NeigRows)):
				if NeigRows[i].startswith(neigIP):
					vplsconnrow = NeigRows[i]
					#crt.Dialog.MessageBox(str(vplsconnrow))


			vlanNums = crt.Dialog.Prompt("Please Enter affected VLANs seperating with space :","Ahmed Elaraby")
			VLANs = vlanNums.split()
			MXMACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 1751 and int(VlanNum) <= 1770:
						
					crt.Screen.Send("show vpls mac-table instance ETISALAT-MOB-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if "lsi" in VLANRows[j]:
							MXMACs.append("There is MAC from Interconnection side [ETISALAT] for VLAN " + VlanNum)

						if link +".1751" in VLANRows[j]:
							MXMACs.append("There is MAC from Customer side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					MXMACs.append(addVlan)

			MACsPr1 = "-"
			MXMACs = list(dict.fromkeys(MXMACs))
			for i in range (0, len(MXMACs)):
				MACsPr1 = MACsPr1 + MXMACs[i] + "\r"

			MACsPr = "- NO MACs received from both side" if MACsPr1 == "-" else MACsPr1

			crt.Screen.Send("show interfaces lo0.0\r")
			crt.Screen.WaitForString("Local: ")
			MXRouterIP = crt.Screen.ReadString("\r").strip()
			#crt.Dialog.MessageBox(MXRouterIP)

			crt.Screen.Send("quit\r")
			crt.Screen.WaitForString("~]$")
			if neigIP == "@":
				crt.Screen.Send("alias " + InterRouter + "\r")
				crt.Screen.WaitForString("telnet")
				neigIP = crt.Screen.ReadString("'").strip()
				crt.Screen.WaitForString("~]$")

			crt.Screen.Send("telnet " + neigIP + "\r")
			crt.Screen.WaitForString("login:")
			crt.Screen.Send(user+"\r")
			crt.Screen.WaitForString("Password:")
			crt.Screen.Send(pass1+"\r")
			crt.Screen.WaitForString("EG>")

			if Port2 != "@" :
				crt.Screen.Send("show interfaces " + Port1 + " terse\r")
				#crt.Screen.WaitForString("--> ")
				WaPo = crt.Screen.WaitForStrings(['--> ','vpls','EG>'],5)
				if WaPo == 1:
					Port1 = crt.Screen.ReadString(".")
					GetINTPort = 0
				if WaPo == 2:
					GetINTPort = 1
				if WaPo == 3:
					crt.Screen.Send("\r")
					GetINTPort = 1
				crt.Screen.WaitForString("EG>")

			

			crt.Screen.Send('show configuration routing-instances ETISALAT-MOB-BITSTREAM | except "ETISALAT-MOB-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			IVPLSRows = []
			IVconfRow = crt.Screen.CurrentRow - 1
			readIVconfRow = crt.Screen.Get(IVconfRow, 1,IVconfRow,400).strip()
			IVPLSRows.append(readIVconfRow)

			while readIVconfRow.endswith("display set") == False:
				IVconfRow = IVconfRow - 1
				readIVconfRow = crt.Screen.Get(IVconfRow, 1,IVconfRow,400).strip()
				IVPLSRows.append(readIVconfRow)

			IVconfRow1 = "set routing-instances ETISALAT-MOB-BITSTREAM protocols vpls enable-mac-move-action"
			IVconfRow2 = "set routing-instances ETISALAT-MOB-BITSTREAM protocols vpls mac-table-size 2000"
			IVconfRow3 = "set routing-instances ETISALAT-MOB-BITSTREAM protocols vpls no-tunnel-services"
			IVconfRow4 = "set routing-instances ETISALAT-MOB-BITSTREAM protocols vpls vpls-id 1751"
			IVconfRow5 = "set routing-instances ETISALAT-MOB-BITSTREAM instance-type vpls"
			IVconfRow6 = "set routing-instances ETISALAT-MOB-BITSTREAM vlan-id all"
			IVconfRow7 = "set routing-instances ETISALAT-MOB-BITSTREAM protocols vpls interface"

			IVconfRow = [IVconfRow1 , IVconfRow2 , IVconfRow3 , IVconfRow4 , IVconfRow5 , IVconfRow6 , IVconfRow7]

			IVcRow = [0,0,0,0,0,0,0]
			for i in range (0, len(IVPLSRows)):
				if IVPLSRows[i] == IVconfRow[0]:
					IVcRow[0] = 1
				if IVPLSRows[i] == IVconfRow[1]:
					IVcRow[1] = 1
				if IVPLSRows[i] == IVconfRow[2]:
					IVcRow[2] = 1
				if IVPLSRows[i] == IVconfRow[3]:
					IVcRow[3] = 1
				if IVPLSRows[i] == IVconfRow[4]:
					IVcRow[4] = 1
				if IVPLSRows[i] == IVconfRow[5]:
					IVcRow[5] = 1
				if IVPLSRows[i].startswith(IVconfRow[6]) == True:
					IVcRow[6] = 1
					interPort0 = IVPLSRows[i].split("interface ")
					interPort1 = interPort0[1].split(".")
					interPort = interPort1[0]
					#crt.Dialog.MessageBox(str(interPort))
					if Port1 != interPort:
						Port1 = interPort
					GetINTPort = 0

			IVcRowPr1 = "-"
			for i in range (0, len(IVcRow)):
				if IVcRow[i] == 0:
					IVcRowPr1 = IVcRowPr1 + IVconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			IVcRowPr = "- NO Missing configuration" if IVcRowPr1 == "-" else IVcRowPr1

			if GetINTPort == 1:
				crt.Screen.Send("show vpls mac-table instance ETISALAT-MOB-BITSTREAM | no-more\r")
				crt.Screen.WaitForString("Routing instance : ETISALAT-MOB-BITSTREAM")
				readINTPortST = crt.Screen.ReadString("MAC flags")
				readINTPortrows = readINTPortST.splitlines()
				#readINTPortrows = [item.strip() for item in readINTPortrows]
				for i in range (0, len(readINTPortrows)):
					if ".1751" in readINTPortrows[i]:
						readINTPortrow1 = readINTPortrows[i]
						readINTPortrow2 = readINTPortrow1.split("D")
						readINTPortrow = readINTPortrow2[1].strip()
						Port12 = readINTPortrow.split(".")
						Port1 = Port12[0]
				crt.Screen.WaitForString("EG>")


			crt.Screen.Send("show configuration interfaces " + Port1 + ".1751 | display set\r")
			crt.Screen.WaitForString("EG>")

			IRows = []
			IconfRow = crt.Screen.CurrentRow - 1
			readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
			IRows.append(readIconfRow)

			while readIconfRow.endswith("display set") == False:
				IconfRow = IconfRow - 1
				readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
				IRows.append(readIconfRow)

			crt.Screen.Send("show configuration routing-instances ETISALAT-MOB-BITSTREAM interface " + Port1 + ".1751 | display set\r")
			crt.Screen.WaitForString("EG>")

			IconfRow2 = crt.Screen.CurrentRow - 1
			readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
			IRows.append(readIconfRow2)

			while readIconfRow2.endswith("display set") == False:
				IconfRow2 = IconfRow2 - 1
				readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
				IRows.append(readIconfRow2)

			IconfRow1 = "set interfaces " + Port1 + " unit 1751 encapsulation vlan-vpls"
			IconfRow2 = "set interfaces " + Port1 + " unit 1751 vlan-id-range 1751-1770"
			IconfRow3 = "set routing-instances ETISALAT-MOB-BITSTREAM interface " + Port1 + ".1751"
			IconfRow = [IconfRow1,IconfRow2,IconfRow3]
			IcRow = [0,0,0]
			for i in range (0, len(IRows)):
				if IRows[i] == IconfRow[0]:
					IcRow[0] = 1
				if IRows[i] == IconfRow[1]:
					IcRow[1] = 1
				if IRows[i] == IconfRow[2]:
					IcRow[2] = 1

			IcRowPr1 = "-"
			for i in range (0, len(IcRow)):
				if IcRow[i] == 0:
					IcRowPr1 = IcRowPr1 + IconfRow[i] + "\r"
			#crt.Dialog.MessageBox(cRowPr)
			IcRowPr = "- NO Missing configuration" if IcRowPr1 == "-" else IcRowPr1

			"""
			crt.Screen.Send("show vpls connections instance ETISALAT-VPLS-BITSTREAM | no-more\r")
			crt.Screen.WaitForString("EG>")

			INeigRows = []
			INeigRow = crt.Screen.CurrentRow - 1
			readINeigRow = crt.Screen.Get(INeigRow, 1,INeigRow,400).strip()
			INeigRows.append(readINeigRow)

			while readINeigRow.endswith("ETISALAT-VPLS-BITSTREAM") == False:
				INeigRow = INeigRow - 1
				readINeigRow = crt.Screen.Get(INeigRow, 1,INeigRow,400).strip()
				INeigRows.append(readINeigRow)

			for i in range (0, len(INeigRows)):
				if INeigRows[i].startswith(MXRouterIP):
					Ivplsconnrow = INeigRows[i]
					#crt.Dialog.MessageBox(str(vplsconnrow))
			"""

			crt.Screen.Send("show vpls connections instance ETISALAT-MOB-BITSTREAM | no-more\r")
			crt.Screen.WaitForString("ETISALAT-MOB-BITSTREAM")
			OVBRead = crt.Screen.ReadString("EG>")

			INeigRows = OVBRead.splitlines()
			INeigRows = [item.strip() for item in INeigRows]

			for i in range (0, len(INeigRows)):
				if MXRouterIP + "(" in INeigRows[i]:
					Ivplsconnrow = INeigRows[i]
					#crt.Dialog.MessageBox(str(vplsconnrow))

			INTMACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 1751 and int(VlanNum) <= 1770:
						
					crt.Screen.Send("show vpls mac-table instance ETISALAT-MOB-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if "lsi" in VLANRows[j]:
							INTMACs.append("There is MAC from MX Router side [customer] for VLAN " + VlanNum)

						if Port1 +".1751" in VLANRows[j]:
							INTMACs.append("There is MAC from ETISALAT side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					INTMACs.append(addVlan)

			IMACsPr1 = "-"
			INTMACs = list(dict.fromkeys(INTMACs))
			for i in range (0, len(INTMACs)):
				IMACsPr1 = IMACsPr1 + INTMACs[i] + "\r"

			IMACsPr = "- NO MACs received from both side" if IMACsPr1 == "-" else IMACsPr1

			crt.Screen.Send("show interfaces " + Port1 + " | no-more\r")
			crt.Screen.WaitForString("Physical link is")
			InterPortStatus = str(crt.Screen.ReadString("Interface index")).strip()

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match last \r")
			crt.Screen.WaitForString("(")
			InterPortLastFlap = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match rate \r")
			crt.Screen.WaitForString("Input rate")
			InterPortInputRate = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("Output rate")
			InterPortOutputRate = crt.Screen.ReadString(")")


			crt.Dialog.MessageBox("            *****ETISALAT-MOB-BITSTREAM*****\r\r* MX Router : " + AggRouter + "\r\r* MX Port : " + link + "\r\r* Status : UP\r\r* Checking MX Port configuration :\r" + cRowPr + "\r\r* Checking MX VPLS configuration :\r" + VcRowPr + "\r\r* vpls connections Status on MX :\r" + vplsconnrow + "\r\r* MACs on MX : \r" + MACsPr + "\r\r* Interconnection Router : "+ InterRouter + "\r\r* Interconnection Port : " + Port1 + "\r\r* Status : " + InterPortStatus + "\r\r* Last Flap : " + InterPortLastFlap + "\r\r* Input Rate" + InterPortInputRate + ")\r* Output Rate" + InterPortOutputRate + ")\r\r* Checking Interconnection Port configuration :\r" + IcRowPr + "\r\r* Checking Interconnection VPLS configuration :\r" + IVcRowPr + "\r\r* vpls connections Status on Interconnection :\r" + Ivplsconnrow + "\r\r* MACs on Interconnection : \r" + IMACsPr ,"Ahmed Elaraby", BUTTON_CANCEL + ICON_INFO)


#######################################################################################################    
########################################### VODAFONE ##################################################
#######################################################################################################

def VODAFONE(user,pass1,link,AggRouter,InterRouter,Port1,Port2):
	crt.Screen.Send("show interfaces descriptions | match " + link + ".2550\r")
	crt.Screen.WaitForString("EG>")

	StatusRows = []
	PortRow = crt.Screen.CurrentRow - 1
	readPortRow1 = crt.Screen.Get(PortRow, 1,PortRow,200).strip()
	StatusRows.append(readPortRow1)

	while readPortRow1.endswith("2550") == False:
		PortRow = PortRow - 1
		readPortRow1 = crt.Screen.Get(PortRow, 1,PortRow,400).strip()
		StatusRows.append(readPortRow1)

	for i in range (0, len(StatusRows)):
		if StatusRows[i].startswith(link):
			readPortRow = StatusRows[i]


	if "up    down" in readPortRow :
		#crt.Dialog.MessageBox("up    down")
		crt.Screen.Send("clear vpls mac-move-action interface " + link + ".2550\r")
		crt.Dialog.MessageBox("check now as mac-move-action cleared")
		return 0
	if "down  up" in readPortRow :
		crt.Dialog.MessageBox("check port is disabled")
		return 0

	if "up    up" in readPortRow :
		#crt.Dialog.MessageBox("up    up")
		crt.Screen.Send("show configuration interfaces " + link + ".2550 | display set\r")
		crt.Screen.WaitForString("EG>")

		Rows = []
		confRow = crt.Screen.CurrentRow - 1
		readconfRow = crt.Screen.Get(confRow, 1,confRow,400).strip()
		Rows.append(readconfRow)

		while readconfRow.endswith("display set") == False:
			confRow = confRow - 1
			readconfRow = crt.Screen.Get(confRow, 1,confRow,400).strip()
			Rows.append(readconfRow)

		crt.Screen.Send("show configuration routing-instances VODA-VPLS-BITSTREAM interface " + link + ".2550 | display set\r")
		crt.Screen.WaitForString("EG>")

		confRow2 = crt.Screen.CurrentRow - 1
		readconfRow2 = crt.Screen.Get(confRow2, 1,confRow2,400).strip()
		Rows.append(readconfRow2)

		while readconfRow2.endswith("display set") == False:
			confRow2 = confRow2 - 1
			readconfRow2 = crt.Screen.Get(confRow2, 1,confRow2,400).strip()
			Rows.append(readconfRow2)


		confRow1 = "set interfaces " + link + " unit 2550 encapsulation vlan-vpls"
		confRow2 = "set interfaces " + link + " unit 2550 vlan-id-range 2550-2799"
		confRow3 = "set routing-instances VODA-VPLS-BITSTREAM interface " + link + ".2550"
		confRow = [confRow1,confRow2,confRow3]
		cRow = [0,0,0]
		for i in range (0, len(Rows)):
			if Rows[i] == confRow[0]:
				cRow[0] = 1
			if Rows[i] == confRow[1]:
				cRow[1] = 1
			if Rows[i] == confRow[2]:
				cRow[2] = 1

		cRowPr1 = "-"
		for i in range (0, len(cRow)):
			if cRow[i] == 0:
				cRowPr1 = cRowPr1 + confRow[i] + "\r"
		#crt.Dialog.MessageBox(cRowPr)
		cRowPr = "- NO Missing configuration" if cRowPr1 == "-" else cRowPr1


		if AggRouter == InterRouter :

			if Port2 != "@" :
				crt.Screen.Send("show interfaces " + Port1 + " terse\r")
				#crt.Screen.WaitForString("--> ")
				WaPo = crt.Screen.WaitForStrings(['--> ','vpls','EG>'],5)
				if WaPo == 1:
					Port1 = crt.Screen.ReadString(".")
					GetINTPort = 0
				if WaPo == 2:
					GetINTPort = 1
				if WaPo == 3:
					crt.Screen.Send("\r")
					GetINTPort = 1
				crt.Screen.WaitForString("EG>")

			crt.Screen.Send('show configuration routing-instances VODA-VPLS-BITSTREAM | except "VODA-VPLS-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			VPLSRows = []
			VconfRow = crt.Screen.CurrentRow - 1
			readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
			VPLSRows.append(readVconfRow)

			while readVconfRow.endswith("display set") == False:
				VconfRow = VconfRow - 1
				readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
				VPLSRows.append(readVconfRow)

			VconfRow1 = "set routing-instances VODA-VPLS-BITSTREAM protocols vpls enable-mac-move-action"
			VconfRow2 = "set routing-instances VODA-VPLS-BITSTREAM protocols vpls mac-table-size 2000"
			VconfRow3 = "set routing-instances VODA-VPLS-BITSTREAM protocols vpls no-tunnel-services"
			VconfRow4 = "set routing-instances VODA-VPLS-BITSTREAM protocols vpls vpls-id 2550"
			VconfRow5 = "set routing-instances VODA-VPLS-BITSTREAM instance-type vpls"
			VconfRow6 = "set routing-instances VODA-VPLS-BITSTREAM vlan-id all"
			VconfRow7 = "set routing-instances VODA-VPLS-BITSTREAM protocols vpls interface"

			VconfRow = [VconfRow1 , VconfRow2 , VconfRow3 , VconfRow4 , VconfRow5 , VconfRow6 , VconfRow7]

			VcRow = [0,0,0,0,0,0,0]
			for i in range (0, len(VPLSRows)):
				if VPLSRows[i] == VconfRow[0]:
					VcRow[0] = 1
				if VPLSRows[i] == VconfRow[1]:
					VcRow[1] = 1
				if VPLSRows[i] == VconfRow[2]:
					VcRow[2] = 1
				if VPLSRows[i] == VconfRow[3]:
					VcRow[3] = 1
				if VPLSRows[i] == VconfRow[4]:
					VcRow[4] = 1
				if VPLSRows[i] == VconfRow[5]:
					VcRow[5] = 1
				if VPLSRows[i].startswith(VconfRow[6]) == True:
					VcRow[6] = 1
					interPort0 = VPLSRows[i].split("interface ")
					interPort1 = interPort0[1].split(".")
					interPort = interPort1[0]
					#crt.Dialog.MessageBox(str(interPort))
					if Port1 != interPort:
						Port1 = interPort
					GetINTPort = 0

			VcRowPr1 = "-"
			for i in range (0, len(VcRow)):
				if VcRow[i] == 0:
					VcRowPr1 = VcRowPr1 + VconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			VcRowPr = "- NO Missing configuration" if VcRowPr1 == "-" else VcRowPr1

			if GetINTPort == 1:
				crt.Screen.Send("show vpls mac-table instance VODA-VPLS-BITSTREAM | no-more\r")
				crt.Screen.WaitForString("Routing instance : VODA-VPLS-BITSTREAM")
				readINTPortST = crt.Screen.ReadString("MAC flags")
				readINTPortrows = readINTPortST.splitlines()
				#readINTPortrows = [item.strip() for item in readINTPortrows]
				for i in range (0, len(readINTPortrows)):
					if ".2550" in readINTPortrows[i]:
						readINTPortrow1 = readINTPortrows[i]
						readINTPortrow2 = readINTPortrow1.split("D")
						readINTPortrow = readINTPortrow2[1].strip()
						Port12 = readINTPortrow.split(".")
						Port1 = Port12[0]
				crt.Screen.WaitForString("EG>")

			crt.Screen.Send("show configuration interfaces " + Port1 + ".2550 | display set\r")
			crt.Screen.WaitForString("EG>")

			IRows = []
			IconfRow = crt.Screen.CurrentRow - 1
			readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
			IRows.append(readIconfRow)

			while readIconfRow.endswith("display set") == False:
				IconfRow = IconfRow - 1
				readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
				IRows.append(readIconfRow)

			crt.Screen.Send("show configuration routing-instances VODA-VPLS-BITSTREAM interface " + Port1 + ".2550 | display set\r")
			crt.Screen.WaitForString("EG>")

			IconfRow2 = crt.Screen.CurrentRow - 1
			readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
			IRows.append(readIconfRow2)

			while readIconfRow2.endswith("display set") == False:
				IconfRow2 = IconfRow2 - 1
				readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
				IRows.append(readIconfRow2)

			IconfRow1 = "set interfaces " + Port1 + " unit 2550 encapsulation vlan-vpls"
			IconfRow2 = "set interfaces " + Port1 + " unit 2550 vlan-id-range 2550-2799"
			IconfRow3 = "set routing-instances VODA-VPLS-BITSTREAM interface " + Port1 + ".2550"
			IconfRow = [IconfRow1,IconfRow2,IconfRow3]
			IcRow = [0,0,0]
			for i in range (0, len(IRows)):
				if IRows[i] == IconfRow[0]:
					IcRow[0] = 1
				if IRows[i] == IconfRow[1]:
					IcRow[1] = 1
				if IRows[i] == IconfRow[2]:
					IcRow[2] = 1

			IcRowPr1 = "-"
			for i in range (0, len(IcRow)):
				if IcRow[i] == 0:
					IcRowPr1 = IcRowPr1 + IconfRow[i] + "\r"
			#crt.Dialog.MessageBox(cRowPr)
			IcRowPr = "- NO Missing configuration" if IcRowPr1 == "-" else IcRowPr1


			vlanNums = crt.Dialog.Prompt("Please Enter affected VLANs seperating with space :","Ahmed Elaraby")
			VLANs = vlanNums.split()
			MACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 2550 and int(VlanNum) <= 2799:
						
					crt.Screen.Send("show vpls mac-table instance VODA-VPLS-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if Port1 + ".2550" in VLANRows[j]:
							MACs.append("There is MAC from VODAFONE side for VLAN " + VlanNum)

						if link +".2550" in VLANRows[j]:
							MACs.append("There is MAC from Customer side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					MACs.append(addVlan)

			MACsPr1 = "-"
			MACs = list(dict.fromkeys(MACs))
			for i in range (0, len(MACs)):
				MACsPr1 = MACsPr1 + MACs[i] + "\r"

			MACsPr = "- NO MACs received from both side" if MACsPr1 == "-" else MACsPr1

			crt.Screen.Send("show interfaces " + Port1 + " | no-more\r")
			crt.Screen.WaitForString("Physical link is")
			InterPortStatus = str(crt.Screen.ReadString("Interface index")).strip()

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match last \r")
			crt.Screen.WaitForString("(")
			InterPortLastFlap = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match rate \r")
			crt.Screen.WaitForString("Input rate")
			InterPortInputRate = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("Output rate")
			InterPortOutputRate = crt.Screen.ReadString(")")




			crt.Dialog.MessageBox("            *****VODA-VPLS-BITSTREAM*****\r\r* MX Router : " + AggRouter + "\r\r* MX Port : " + link + "\r\r* Status : UP\r\r* Checking MX Port configuration :\r" + cRowPr +  "\r\r* Checking VPLS configuration :\r" + VcRowPr + "\r\r* Interconnection Router : "+ InterRouter + "\r\r* Interconnection Port : " + Port1 + "\r\r* Status : " + InterPortStatus + "\r\r* Last Flap : " + InterPortLastFlap + "\r\r* Input Rate" + InterPortInputRate + ")\r* Output Rate" + InterPortOutputRate + ")\r\r* MACs : \r" + MACsPr ,"Ahmed Elaraby", BUTTON_CANCEL + ICON_INFO)



		if AggRouter != InterRouter :
			#crt.Dialog.MessageBox("AggRouter != InterRouter")
			crt.Screen.Send('show configuration routing-instances VODA-VPLS-BITSTREAM | except "VODA-VPLS-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			VPLSRows = []
			VconfRow = crt.Screen.CurrentRow - 1
			readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
			VPLSRows.append(readVconfRow)

			while readVconfRow.endswith("display set") == False:
				VconfRow = VconfRow - 1
				readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
				VPLSRows.append(readVconfRow)

			VconfRow1 = "set routing-instances VODA-VPLS-BITSTREAM protocols vpls enable-mac-move-action"
			VconfRow2 = "set routing-instances VODA-VPLS-BITSTREAM protocols vpls mac-table-size 2000"
			VconfRow3 = "set routing-instances VODA-VPLS-BITSTREAM protocols vpls no-tunnel-services"
			VconfRow4 = "set routing-instances VODA-VPLS-BITSTREAM protocols vpls vpls-id 2550"
			VconfRow5 = "set routing-instances VODA-VPLS-BITSTREAM instance-type vpls"
			VconfRow6 = "set routing-instances VODA-VPLS-BITSTREAM vlan-id all"
			VconfRow7 = "set routing-instances VODA-VPLS-BITSTREAM protocols vpls neighbor"

			VconfRow = [VconfRow1 , VconfRow2 , VconfRow3 , VconfRow4 , VconfRow5 , VconfRow6 , VconfRow7]

			VcRow = [0,0,0,0,0,0,0]
			neigIP = "@"
			for i in range (0, len(VPLSRows)):
				if VPLSRows[i] == VconfRow[0]:
					VcRow[0] = 1
				if VPLSRows[i] == VconfRow[1]:
					VcRow[1] = 1
				if VPLSRows[i] == VconfRow[2]:
					VcRow[2] = 1
				if VPLSRows[i] == VconfRow[3]:
					VcRow[3] = 1
				if VPLSRows[i] == VconfRow[4]:
					VcRow[4] = 1
				if VPLSRows[i] == VconfRow[5]:
					VcRow[5] = 1
				if VPLSRows[i].startswith(VconfRow[6]) == True:
					VcRow[6] = 1
					neigIP0 = VPLSRows[i].split("neighbor ")
					neigIP1 = neigIP0[1].split(" ")
					neigIP = neigIP1[0]

			"""
			if neigIP == "@":

				data =[]
				FileName = "Devices.csv"
				try:
					with open(os.path.join(os.path.dirname(__file__), FileName), mode='r') as csvfile:
						reader = csv.reader(csvfile)
						for row in reader:
							data.append(row)
				except EnvironmentError:
					crt.Dialog.MessageBox("Sorry Can't Open File! Please Change Files and Script Location!","Ahmed Elaraby")
					return 0

				TARGETCICol = [x[11] for x in data]
				if InterRouter in TARGETCICol:
					for x in range(0,len(data)):
						if InterRouter == data[x][11]:
							neigIP = data[x][5]

			"""

			VcRowPr1 = "-"
			for i in range (0, len(VcRow)):
				if VcRow[i] == 0:
					VcRowPr1 = VcRowPr1 + VconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			VcRowPr = "- NO Missing configuration" if VcRowPr1 == "-" else VcRowPr1

			crt.Screen.Send("show vpls connections instance VODA-VPLS-BITSTREAM | no-more\r")
			crt.Screen.WaitForString("EG>")

			NeigRows = []
			NeigRow = crt.Screen.CurrentRow - 1
			readNeigRow = crt.Screen.Get(NeigRow, 1,NeigRow,400).strip()
			NeigRows.append(readNeigRow)

			while readNeigRow.endswith("VODA-VPLS-BITSTREAM") == False:
				NeigRow = NeigRow - 1
				readNeigRow = crt.Screen.Get(NeigRow, 1,NeigRow,400).strip()
				NeigRows.append(readNeigRow)

			for i in range (0, len(NeigRows)):
				if NeigRows[i].startswith(neigIP):
					vplsconnrow = NeigRows[i]
					#crt.Dialog.MessageBox(str(vplsconnrow))


			vlanNums = crt.Dialog.Prompt("Please Enter affected VLANs seperating with space :","Ahmed Elaraby")
			VLANs = vlanNums.split()
			MXMACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 2550 and int(VlanNum) <= 2799:
						
					crt.Screen.Send("show vpls mac-table instance VODA-VPLS-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if "lsi" in VLANRows[j]:
							MXMACs.append("There is MAC from Interconnection side [VODAFONE] for VLAN " + VlanNum)

						if link +".2550" in VLANRows[j]:
							MXMACs.append("There is MAC from Customer side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					MXMACs.append(addVlan)

			MACsPr1 = "-"
			MXMACs = list(dict.fromkeys(MXMACs))
			for i in range (0, len(MXMACs)):
				MACsPr1 = MACsPr1 + MXMACs[i] + "\r"

			MACsPr = "- NO MACs received from both side" if MACsPr1 == "-" else MACsPr1

			crt.Screen.Send("show interfaces lo0.0\r")
			crt.Screen.WaitForString("Local: ")
			MXRouterIP = crt.Screen.ReadString("\r").strip()
			#crt.Dialog.MessageBox(MXRouterIP)

			crt.Screen.Send("quit\r")
			crt.Screen.WaitForString("~]$")

			if neigIP == "@":
				crt.Screen.Send("alias " + InterRouter + "\r")
				crt.Screen.WaitForString("telnet")
				neigIP = crt.Screen.ReadString("'").strip()
				crt.Screen.WaitForString("~]$")

			crt.Screen.Send("telnet " + neigIP + "\r")
			crt.Screen.WaitForString("login:")
			crt.Screen.Send(user+"\r")
			crt.Screen.WaitForString("Password:")
			crt.Screen.Send(pass1+"\r")
			crt.Screen.WaitForString("EG>")

			if Port2 != "@" :
				crt.Screen.Send("show interfaces " + Port1 + " terse\r")
				#crt.Screen.WaitForString("--> ")
				WaPo = crt.Screen.WaitForStrings(['--> ','vpls','EG>'],5)
				if WaPo == 1:
					Port1 = crt.Screen.ReadString(".")
					GetINTPort = 0
				if WaPo == 2:
					GetINTPort = 1
				if WaPo == 3:
					crt.Screen.Send("\r")
					GetINTPort = 1
				crt.Screen.WaitForString("EG>")


			crt.Screen.Send('show configuration routing-instances VODA-VPLS-BITSTREAM | except "VODA-VPLS-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			IVPLSRows = []
			IVconfRow = crt.Screen.CurrentRow - 1
			readIVconfRow = crt.Screen.Get(IVconfRow, 1,IVconfRow,400).strip()
			IVPLSRows.append(readIVconfRow)

			while readIVconfRow.endswith("display set") == False:
				IVconfRow = IVconfRow - 1
				readIVconfRow = crt.Screen.Get(IVconfRow, 1,IVconfRow,400).strip()
				IVPLSRows.append(readIVconfRow)

			IVconfRow1 = "set routing-instances VODA-VPLS-BITSTREAM protocols vpls enable-mac-move-action"
			IVconfRow2 = "set routing-instances VODA-VPLS-BITSTREAM protocols vpls mac-table-size 2000"
			IVconfRow3 = "set routing-instances VODA-VPLS-BITSTREAM protocols vpls no-tunnel-services"
			IVconfRow4 = "set routing-instances VODA-VPLS-BITSTREAM protocols vpls vpls-id 2550"
			IVconfRow5 = "set routing-instances VODA-VPLS-BITSTREAM instance-type vpls"
			IVconfRow6 = "set routing-instances VODA-VPLS-BITSTREAM vlan-id all"
			IVconfRow7 = "set routing-instances VODA-VPLS-BITSTREAM protocols vpls interface"

			IVconfRow = [IVconfRow1 , IVconfRow2 , IVconfRow3 , IVconfRow4 , IVconfRow5 , IVconfRow6 , IVconfRow7]

			IVcRow = [0,0,0,0,0,0,0]
			for i in range (0, len(IVPLSRows)):
				if IVPLSRows[i] == IVconfRow[0]:
					IVcRow[0] = 1
				if IVPLSRows[i] == IVconfRow[1]:
					IVcRow[1] = 1
				if IVPLSRows[i] == IVconfRow[2]:
					IVcRow[2] = 1
				if IVPLSRows[i] == IVconfRow[3]:
					IVcRow[3] = 1
				if IVPLSRows[i] == IVconfRow[4]:
					IVcRow[4] = 1
				if IVPLSRows[i] == IVconfRow[5]:
					IVcRow[5] = 1
				if IVPLSRows[i].startswith(IVconfRow[6]) == True:
					IVcRow[6] = 1
					interPort0 = IVPLSRows[i].split("interface ")
					interPort1 = interPort0[1].split(".")
					interPort = interPort1[0]
					#crt.Dialog.MessageBox(str(interPort))
					if Port1 != interPort:
						Port1 = interPort
					GetINTPort = 0

			IVcRowPr1 = "-"
			for i in range (0, len(IVcRow)):
				if IVcRow[i] == 0:
					IVcRowPr1 = IVcRowPr1 + IVconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			IVcRowPr = "- NO Missing configuration" if IVcRowPr1 == "-" else IVcRowPr1

			if GetINTPort == 1:
				crt.Screen.Send("show vpls mac-table instance VODA-VPLS-BITSTREAM | no-more\r")
				crt.Screen.WaitForString("Routing instance : VODA-VPLS-BITSTREAM")
				readINTPortST = crt.Screen.ReadString("MAC flags")
				readINTPortrows = readINTPortST.splitlines()
				#readINTPortrows = [item.strip() for item in readINTPortrows]
				for i in range (0, len(readINTPortrows)):
					if ".2550" in readINTPortrows[i]:
						readINTPortrow1 = readINTPortrows[i]
						readINTPortrow2 = readINTPortrow1.split("D")
						readINTPortrow = readINTPortrow2[1].strip()
						Port12 = readINTPortrow.split(".")
						Port1 = Port12[0]
				crt.Screen.WaitForString("EG>")

			crt.Screen.Send("show configuration interfaces " + Port1 + ".2550 | display set\r")
			crt.Screen.WaitForString("EG>")

			IRows = []
			IconfRow = crt.Screen.CurrentRow - 1
			readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
			IRows.append(readIconfRow)

			while readIconfRow.endswith("display set") == False:
				IconfRow = IconfRow - 1
				readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
				IRows.append(readIconfRow)

			crt.Screen.Send("show configuration routing-instances VODA-VPLS-BITSTREAM interface " + Port1 + ".2550 | display set\r")
			crt.Screen.WaitForString("EG>")

			IconfRow2 = crt.Screen.CurrentRow - 1
			readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
			IRows.append(readIconfRow2)

			while readIconfRow2.endswith("display set") == False:
				IconfRow2 = IconfRow2 - 1
				readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
				IRows.append(readIconfRow2)

			IconfRow1 = "set interfaces " + Port1 + " unit 2550 encapsulation vlan-vpls"
			IconfRow2 = "set interfaces " + Port1 + " unit 2550 vlan-id-range 2550-2799"
			IconfRow3 = "set routing-instances VODA-VPLS-BITSTREAM interface " + Port1 + ".2550"
			IconfRow = [IconfRow1,IconfRow2,IconfRow3]
			IcRow = [0,0,0]
			for i in range (0, len(IRows)):
				if IRows[i] == IconfRow[0]:
					IcRow[0] = 1
				if IRows[i] == IconfRow[1]:
					IcRow[1] = 1
				if IRows[i] == IconfRow[2]:
					IcRow[2] = 1

			IcRowPr1 = "-"
			for i in range (0, len(IcRow)):
				if IcRow[i] == 0:
					IcRowPr1 = IcRowPr1 + IconfRow[i] + "\r"
			#crt.Dialog.MessageBox(cRowPr)
			IcRowPr = "- NO Missing configuration" if IcRowPr1 == "-" else IcRowPr1

			"""
			crt.Screen.Send("show vpls connections instance VODA-VPLS-BITSTREAM | no-more\r")
			crt.Screen.WaitForString("EG>")

			INeigRows = []
			INeigRow = crt.Screen.CurrentRow - 1
			readINeigRow = crt.Screen.Get(INeigRow, 1,INeigRow,400).strip()
			INeigRows.append(readINeigRow)

			while readINeigRow.endswith("VODA-VPLS-BITSTREAM") == False:
				INeigRow = INeigRow - 1
				readINeigRow = crt.Screen.Get(INeigRow, 1,INeigRow,400).strip()
				INeigRows.append(readINeigRow)

			for i in range (0, len(INeigRows)):
				if INeigRows[i].startswith(MXRouterIP):
					Ivplsconnrow = INeigRows[i]
					#crt.Dialog.MessageBox(str(vplsconnrow))
			"""
			crt.Screen.Send("show vpls connections instance VODA-VPLS-BITSTREAM | no-more\r")
			crt.Screen.WaitForString("VODA-VPLS-BITSTREAM")
			OVBRead = crt.Screen.ReadString("EG>")

			INeigRows = OVBRead.splitlines()
			INeigRows = [item.strip() for item in INeigRows]

			for i in range (0, len(INeigRows)):
				if MXRouterIP + "(" in INeigRows[i]:
					Ivplsconnrow = INeigRows[i]
					#crt.Dialog.MessageBox(str(vplsconnrow))


			INTMACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 2550 and int(VlanNum) <= 2799:
						
					crt.Screen.Send("show vpls mac-table instance VODA-VPLS-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if "lsi" in VLANRows[j]:
							INTMACs.append("There is MAC from MX Router side [customer] for VLAN " + VlanNum)

						if Port1 +".2550" in VLANRows[j]:
							INTMACs.append("There is MAC from VODAFONE side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					INTMACs.append(addVlan)

			IMACsPr1 = "-"
			INTMACs = list(dict.fromkeys(INTMACs))
			for i in range (0, len(INTMACs)):
				IMACsPr1 = IMACsPr1 + INTMACs[i] + "\r"

			IMACsPr = "- NO MACs received from both side" if IMACsPr1 == "-" else IMACsPr1

			crt.Screen.Send("show interfaces " + Port1 + " | no-more\r")
			crt.Screen.WaitForString("Physical link is")
			InterPortStatus = str(crt.Screen.ReadString("Interface index")).strip()

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match last \r")
			crt.Screen.WaitForString("(")
			InterPortLastFlap = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match rate \r")
			crt.Screen.WaitForString("Input rate")
			InterPortInputRate = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("Output rate")
			InterPortOutputRate = crt.Screen.ReadString(")")


			crt.Dialog.MessageBox("            *****VODA-VPLS-BITSTREAM*****\r\r* MX Router : " + AggRouter + "\r\r* MX Port : " + link + "\r\r* Status : UP\r\r* Checking MX Port configuration :\r" + cRowPr + "\r\r* Checking MX VPLS configuration :\r" + VcRowPr + "\r\r* vpls connections Status on MX :\r" + vplsconnrow + "\r\r* MACs on MX : \r" + MACsPr + "\r\r* Interconnection Router : "+ InterRouter + "\r\r* Interconnection Port : " + Port1 + "\r\r* Status : " + InterPortStatus + "\r\r* Last Flap : " + InterPortLastFlap + "\r\r* Input Rate" + InterPortInputRate + ")\r* Output Rate" + InterPortOutputRate + ")\r\r* Checking Interconnection Port configuration :\r" + IcRowPr + "\r\r* Checking Interconnection VPLS configuration :\r" + IVcRowPr + "\r\r* vpls connections Status on Interconnection :\r" + Ivplsconnrow + "\r\r* MACs on Interconnection : \r" + IMACsPr ,"Ahmed Elaraby", BUTTON_CANCEL + ICON_INFO)


#######################################################################################################    
########################################### VODAFONE Mobile ###########################################
#######################################################################################################

def VODAFONEMOB(user,pass1,link,AggRouter,InterRouter,Port1,Port2):
	crt.Screen.Send("show interfaces descriptions | match " + link + ".2050\r")
	crt.Screen.WaitForString("EG>")

	StatusRows = []
	PortRow = crt.Screen.CurrentRow - 1
	readPortRow1 = crt.Screen.Get(PortRow, 1,PortRow,200).strip()
	StatusRows.append(readPortRow1)

	while readPortRow1.endswith("2050") == False:
		PortRow = PortRow - 1
		readPortRow1 = crt.Screen.Get(PortRow, 1,PortRow,400).strip()
		StatusRows.append(readPortRow1)

	for i in range (0, len(StatusRows)):
		if StatusRows[i].startswith(link):
			readPortRow = StatusRows[i]


	if "up    down" in readPortRow :
		#crt.Dialog.MessageBox("up    down")
		crt.Screen.Send("clear vpls mac-move-action interface " + link + ".2050\r")
		crt.Dialog.MessageBox("check now as mac-move-action cleared")
		return 0
	if "down  up" in readPortRow :
		crt.Dialog.MessageBox("check port is disabled")
		return 0

	if "up    up" in readPortRow :
		#crt.Dialog.MessageBox("up    up")
		crt.Screen.Send("show configuration interfaces " + link + ".2050 | display set\r")
		crt.Screen.WaitForString("EG>")

		Rows = []
		confRow = crt.Screen.CurrentRow - 1
		readconfRow = crt.Screen.Get(confRow, 1,confRow,400).strip()
		Rows.append(readconfRow)

		while readconfRow.endswith("display set") == False:
			confRow = confRow - 1
			readconfRow = crt.Screen.Get(confRow, 1,confRow,400).strip()
			Rows.append(readconfRow)

		crt.Screen.Send("show configuration routing-instances VODA-MOB-BITSTREAM interface " + link + ".2050 | display set\r")
		crt.Screen.WaitForString("EG>")

		confRow2 = crt.Screen.CurrentRow - 1
		readconfRow2 = crt.Screen.Get(confRow2, 1,confRow2,400).strip()
		Rows.append(readconfRow2)

		while readconfRow2.endswith("display set") == False:
			confRow2 = confRow2 - 1
			readconfRow2 = crt.Screen.Get(confRow2, 1,confRow2,400).strip()
			Rows.append(readconfRow2)


		confRow1 = "set interfaces " + link + " unit 2050 encapsulation vlan-vpls"
		confRow2 = "set interfaces " + link + " unit 2050 vlan-id-range 2050-2099"
		confRow3 = "set routing-instances VODA-MOB-BITSTREAM interface " + link + ".2050"
		confRow = [confRow1,confRow2,confRow3]
		cRow = [0,0,0]
		for i in range (0, len(Rows)):
			if Rows[i] == confRow[0]:
				cRow[0] = 1
			if Rows[i] == confRow[1]:
				cRow[1] = 1
			if Rows[i] == confRow[2]:
				cRow[2] = 1

		cRowPr1 = "-"
		for i in range (0, len(cRow)):
			if cRow[i] == 0:
				cRowPr1 = cRowPr1 + confRow[i] + "\r"
		#crt.Dialog.MessageBox(cRowPr)
		cRowPr = "- NO Missing configuration" if cRowPr1 == "-" else cRowPr1


		if AggRouter == InterRouter :

			if Port2 != "@" :
				crt.Screen.Send("show interfaces " + Port1 + " terse\r")
				#crt.Screen.WaitForString("--> ")
				WaPo = crt.Screen.WaitForStrings(['--> ','vpls','EG>'],5)
				if WaPo == 1:
					Port1 = crt.Screen.ReadString(".")
					GetINTPort = 0
				if WaPo == 2:
					GetINTPort = 1
				if WaPo == 3:
					crt.Screen.Send("\r")
					GetINTPort = 1
				crt.Screen.WaitForString("EG>")

			crt.Screen.Send('show configuration routing-instances VODA-MOB-BITSTREAM | except "VODA-MOB-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			VPLSRows = []
			VconfRow = crt.Screen.CurrentRow - 1
			readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
			VPLSRows.append(readVconfRow)

			while readVconfRow.endswith("display set") == False:
				VconfRow = VconfRow - 1
				readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
				VPLSRows.append(readVconfRow)

			VconfRow1 = "set routing-instances VODA-MOB-BITSTREAM protocols vpls enable-mac-move-action"
			VconfRow2 = "set routing-instances VODA-MOB-BITSTREAM protocols vpls mac-table-size 2000"
			VconfRow3 = "set routing-instances VODA-MOB-BITSTREAM protocols vpls no-tunnel-services"
			VconfRow4 = "set routing-instances VODA-MOB-BITSTREAM protocols vpls vpls-id 2050"
			VconfRow5 = "set routing-instances VODA-MOB-BITSTREAM instance-type vpls"
			VconfRow6 = "set routing-instances VODA-MOB-BITSTREAM vlan-id all"
			VconfRow7 = "set routing-instances VODA-MOB-BITSTREAM protocols vpls interface"

			VconfRow = [VconfRow1 , VconfRow2 , VconfRow3 , VconfRow4 , VconfRow5 , VconfRow6 , VconfRow7]

			VcRow = [0,0,0,0,0,0,0]
			for i in range (0, len(VPLSRows)):
				if VPLSRows[i] == VconfRow[0]:
					VcRow[0] = 1
				if VPLSRows[i] == VconfRow[1]:
					VcRow[1] = 1
				if VPLSRows[i] == VconfRow[2]:
					VcRow[2] = 1
				if VPLSRows[i] == VconfRow[3]:
					VcRow[3] = 1
				if VPLSRows[i] == VconfRow[4]:
					VcRow[4] = 1
				if VPLSRows[i] == VconfRow[5]:
					VcRow[5] = 1
				if VPLSRows[i].startswith(VconfRow[6]) == True:
					VcRow[6] = 1
					interPort0 = VPLSRows[i].split("interface ")
					interPort1 = interPort0[1].split(".")
					interPort = interPort1[0]
					#crt.Dialog.MessageBox(str(interPort))
					if Port1 != interPort:
						Port1 = interPort
					GetINTPort = 0

			VcRowPr1 = "-"
			for i in range (0, len(VcRow)):
				if VcRow[i] == 0:
					VcRowPr1 = VcRowPr1 + VconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			VcRowPr = "- NO Missing configuration" if VcRowPr1 == "-" else VcRowPr1

			if GetINTPort == 1:
				crt.Screen.Send("show vpls mac-table instance VODA-MOB-BITSTREAM | no-more\r")
				crt.Screen.WaitForString("Routing instance : VODA-MOB-BITSTREAM")
				readINTPortST = crt.Screen.ReadString("MAC flags")
				readINTPortrows = readINTPortST.splitlines()
				#readINTPortrows = [item.strip() for item in readINTPortrows]
				for i in range (0, len(readINTPortrows)):
					if ".2050" in readINTPortrows[i]:
						readINTPortrow1 = readINTPortrows[i]
						readINTPortrow2 = readINTPortrow1.split("D")
						readINTPortrow = readINTPortrow2[1].strip()
						Port12 = readINTPortrow.split(".")
						Port1 = Port12[0]
				crt.Screen.WaitForString("EG>")

			crt.Screen.Send("show configuration interfaces " + Port1 + ".2050 | display set\r")
			crt.Screen.WaitForString("EG>")

			IRows = []
			IconfRow = crt.Screen.CurrentRow - 1
			readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
			IRows.append(readIconfRow)

			while readIconfRow.endswith("display set") == False:
				IconfRow = IconfRow - 1
				readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
				IRows.append(readIconfRow)

			crt.Screen.Send("show configuration routing-instances VODA-MOB-BITSTREAM interface " + Port1 + ".2050 | display set\r")
			crt.Screen.WaitForString("EG>")

			IconfRow2 = crt.Screen.CurrentRow - 1
			readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
			IRows.append(readIconfRow2)

			while readIconfRow2.endswith("display set") == False:
				IconfRow2 = IconfRow2 - 1
				readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
				IRows.append(readIconfRow2)

			IconfRow1 = "set interfaces " + Port1 + " unit 2050 encapsulation vlan-vpls"
			IconfRow2 = "set interfaces " + Port1 + " unit 2050 vlan-id-range 2050-2099"
			IconfRow3 = "set routing-instances VODA-MOB-BITSTREAM interface " + Port1 + ".2050"
			IconfRow = [IconfRow1,IconfRow2,IconfRow3]
			IcRow = [0,0,0]
			for i in range (0, len(IRows)):
				if IRows[i] == IconfRow[0]:
					IcRow[0] = 1
				if IRows[i] == IconfRow[1]:
					IcRow[1] = 1
				if IRows[i] == IconfRow[2]:
					IcRow[2] = 1

			IcRowPr1 = "-"
			for i in range (0, len(IcRow)):
				if IcRow[i] == 0:
					IcRowPr1 = IcRowPr1 + IconfRow[i] + "\r"
			#crt.Dialog.MessageBox(cRowPr)
			IcRowPr = "- NO Missing configuration" if IcRowPr1 == "-" else IcRowPr1


			vlanNums = crt.Dialog.Prompt("Please Enter affected VLANs seperating with space :","Ahmed Elaraby")
			VLANs = vlanNums.split()
			MACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 2050 and int(VlanNum) <= 2099:
						
					crt.Screen.Send("show vpls mac-table instance VODA-MOB-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if Port1 + ".2050" in VLANRows[j]:
							MACs.append("There is MAC from VODAFONE side for VLAN " + VlanNum)

						if link +".2050" in VLANRows[j]:
							MACs.append("There is MAC from Customer side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					MACs.append(addVlan)

			MACsPr1 = "-"
			MACs = list(dict.fromkeys(MACs))
			for i in range (0, len(MACs)):
				MACsPr1 = MACsPr1 + MACs[i] + "\r"

			MACsPr = "- NO MACs received from both side" if MACsPr1 == "-" else MACsPr1

			crt.Screen.Send("show interfaces " + Port1 + " | no-more\r")
			crt.Screen.WaitForString("Physical link is")
			InterPortStatus = str(crt.Screen.ReadString("Interface index")).strip()

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match last \r")
			crt.Screen.WaitForString("(")
			InterPortLastFlap = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match rate \r")
			crt.Screen.WaitForString("Input rate")
			InterPortInputRate = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("Output rate")
			InterPortOutputRate = crt.Screen.ReadString(")")




			crt.Dialog.MessageBox("            *****VODA-MOB-BITSTREAM*****\r\r* MX Router : " + AggRouter + "\r\r* MX Port : " + link + "\r\r* Status : UP\r\r* Checking MX Port configuration :\r" + cRowPr +  "\r\r* Checking VPLS configuration :\r" + VcRowPr + "\r\r* Interconnection Router : "+ InterRouter + "\r\r* Interconnection Port : " + Port1 + "\r\r* Status : " + InterPortStatus + "\r\r* Last Flap : " + InterPortLastFlap + "\r\r* Input Rate" + InterPortInputRate + ")\r* Output Rate" + InterPortOutputRate + ")\r\r* MACs : \r" + MACsPr ,"Ahmed Elaraby", BUTTON_CANCEL + ICON_INFO)



		if AggRouter != InterRouter :
			#crt.Dialog.MessageBox("AggRouter != InterRouter")
			crt.Screen.Send('show configuration routing-instances VODA-MOB-BITSTREAM | except "VODA-MOB-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			VPLSRows = []
			VconfRow = crt.Screen.CurrentRow - 1
			readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
			VPLSRows.append(readVconfRow)

			while readVconfRow.endswith("display set") == False:
				VconfRow = VconfRow - 1
				readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
				VPLSRows.append(readVconfRow)

			VconfRow1 = "set routing-instances VODA-MOB-BITSTREAM protocols vpls enable-mac-move-action"
			VconfRow2 = "set routing-instances VODA-MOB-BITSTREAM protocols vpls mac-table-size 2000"
			VconfRow3 = "set routing-instances VODA-MOB-BITSTREAM protocols vpls no-tunnel-services"
			VconfRow4 = "set routing-instances VODA-MOB-BITSTREAM protocols vpls vpls-id 2050"
			VconfRow5 = "set routing-instances VODA-MOB-BITSTREAM instance-type vpls"
			VconfRow6 = "set routing-instances VODA-MOB-BITSTREAM vlan-id all"
			VconfRow7 = "set routing-instances VODA-MOB-BITSTREAM protocols vpls neighbor"

			VconfRow = [VconfRow1 , VconfRow2 , VconfRow3 , VconfRow4 , VconfRow5 , VconfRow6 , VconfRow7]

			VcRow = [0,0,0,0,0,0,0]
			neigIP = "@"
			for i in range (0, len(VPLSRows)):
				if VPLSRows[i] == VconfRow[0]:
					VcRow[0] = 1
				if VPLSRows[i] == VconfRow[1]:
					VcRow[1] = 1
				if VPLSRows[i] == VconfRow[2]:
					VcRow[2] = 1
				if VPLSRows[i] == VconfRow[3]:
					VcRow[3] = 1
				if VPLSRows[i] == VconfRow[4]:
					VcRow[4] = 1
				if VPLSRows[i] == VconfRow[5]:
					VcRow[5] = 1
				if VPLSRows[i].startswith(VconfRow[6]) == True:
					VcRow[6] = 1
					neigIP0 = VPLSRows[i].split("neighbor ")
					neigIP1 = neigIP0[1].split(" ")
					neigIP = neigIP1[0]

			"""
			if neigIP == "@":

				data =[]
				FileName = "Devices.csv"
				try:
					with open(os.path.join(os.path.dirname(__file__), FileName), mode='r') as csvfile:
						reader = csv.reader(csvfile)
						for row in reader:
							data.append(row)
				except EnvironmentError:
					crt.Dialog.MessageBox("Sorry Can't Open File! Please Change Files and Script Location!","Ahmed Elaraby")
					return 0

				TARGETCICol = [x[11] for x in data]
				if InterRouter in TARGETCICol:
					for x in range(0,len(data)):
						if InterRouter == data[x][11]:
							neigIP = data[x][5]

			"""

			VcRowPr1 = "-"
			for i in range (0, len(VcRow)):
				if VcRow[i] == 0:
					VcRowPr1 = VcRowPr1 + VconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			VcRowPr = "- NO Missing configuration" if VcRowPr1 == "-" else VcRowPr1

			crt.Screen.Send("show vpls connections instance VODA-MOB-BITSTREAM | no-more\r")
			crt.Screen.WaitForString("EG>")

			NeigRows = []
			NeigRow = crt.Screen.CurrentRow - 1
			readNeigRow = crt.Screen.Get(NeigRow, 1,NeigRow,400).strip()
			NeigRows.append(readNeigRow)

			while readNeigRow.endswith("VODA-MOB-BITSTREAM") == False:
				NeigRow = NeigRow - 1
				readNeigRow = crt.Screen.Get(NeigRow, 1,NeigRow,400).strip()
				NeigRows.append(readNeigRow)

			for i in range (0, len(NeigRows)):
				if NeigRows[i].startswith(neigIP):
					vplsconnrow = NeigRows[i]
					#crt.Dialog.MessageBox(str(vplsconnrow))


			vlanNums = crt.Dialog.Prompt("Please Enter affected VLANs seperating with space :","Ahmed Elaraby")
			VLANs = vlanNums.split()
			MXMACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 2050 and int(VlanNum) <= 2099:
						
					crt.Screen.Send("show vpls mac-table instance VODA-MOB-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if "lsi" in VLANRows[j]:
							MXMACs.append("There is MAC from Interconnection side [VODAFONE] for VLAN " + VlanNum)

						if link +".2050" in VLANRows[j]:
							MXMACs.append("There is MAC from Customer side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					MXMACs.append(addVlan)

			MACsPr1 = "-"
			MXMACs = list(dict.fromkeys(MXMACs))
			for i in range (0, len(MXMACs)):
				MACsPr1 = MACsPr1 + MXMACs[i] + "\r"

			MACsPr = "- NO MACs received from both side" if MACsPr1 == "-" else MACsPr1

			crt.Screen.Send("show interfaces lo0.0\r")
			crt.Screen.WaitForString("Local: ")
			MXRouterIP = crt.Screen.ReadString("\r").strip()
			#crt.Dialog.MessageBox(MXRouterIP)

			crt.Screen.Send("quit\r")
			crt.Screen.WaitForString("~]$")

			if neigIP == "@":
				crt.Screen.Send("alias " + InterRouter + "\r")
				crt.Screen.WaitForString("telnet")
				neigIP = crt.Screen.ReadString("'").strip()
				crt.Screen.WaitForString("~]$")

			crt.Screen.Send("telnet " + neigIP + "\r")
			crt.Screen.WaitForString("login:")
			crt.Screen.Send(user+"\r")
			crt.Screen.WaitForString("Password:")
			crt.Screen.Send(pass1+"\r")
			crt.Screen.WaitForString("EG>")

			if Port2 != "@" :
				crt.Screen.Send("show interfaces " + Port1 + " terse\r")
				#crt.Screen.WaitForString("--> ")
				WaPo = crt.Screen.WaitForStrings(['--> ','vpls','EG>'],5)
				if WaPo == 1:
					Port1 = crt.Screen.ReadString(".")
					GetINTPort = 0
				if WaPo == 2:
					GetINTPort = 1
				if WaPo == 3:
					crt.Screen.Send("\r")
					GetINTPort = 1
				crt.Screen.WaitForString("EG>")


			crt.Screen.Send('show configuration routing-instances VODA-MOB-BITSTREAM | except "VODA-MOB-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			IVPLSRows = []
			IVconfRow = crt.Screen.CurrentRow - 1
			readIVconfRow = crt.Screen.Get(IVconfRow, 1,IVconfRow,400).strip()
			IVPLSRows.append(readIVconfRow)

			while readIVconfRow.endswith("display set") == False:
				IVconfRow = IVconfRow - 1
				readIVconfRow = crt.Screen.Get(IVconfRow, 1,IVconfRow,400).strip()
				IVPLSRows.append(readIVconfRow)

			IVconfRow1 = "set routing-instances VODA-MOB-BITSTREAM protocols vpls enable-mac-move-action"
			IVconfRow2 = "set routing-instances VODA-MOB-BITSTREAM protocols vpls mac-table-size 2000"
			IVconfRow3 = "set routing-instances VODA-MOB-BITSTREAM protocols vpls no-tunnel-services"
			IVconfRow4 = "set routing-instances VODA-MOB-BITSTREAM protocols vpls vpls-id 2050"
			IVconfRow5 = "set routing-instances VODA-MOB-BITSTREAM instance-type vpls"
			IVconfRow6 = "set routing-instances VODA-MOB-BITSTREAM vlan-id all"
			IVconfRow7 = "set routing-instances VODA-MOB-BITSTREAM protocols vpls interface"

			IVconfRow = [IVconfRow1 , IVconfRow2 , IVconfRow3 , IVconfRow4 , IVconfRow5 , IVconfRow6 , IVconfRow7]

			IVcRow = [0,0,0,0,0,0,0]
			for i in range (0, len(IVPLSRows)):
				if IVPLSRows[i] == IVconfRow[0]:
					IVcRow[0] = 1
				if IVPLSRows[i] == IVconfRow[1]:
					IVcRow[1] = 1
				if IVPLSRows[i] == IVconfRow[2]:
					IVcRow[2] = 1
				if IVPLSRows[i] == IVconfRow[3]:
					IVcRow[3] = 1
				if IVPLSRows[i] == IVconfRow[4]:
					IVcRow[4] = 1
				if IVPLSRows[i] == IVconfRow[5]:
					IVcRow[5] = 1
				if IVPLSRows[i].startswith(IVconfRow[6]) == True:
					IVcRow[6] = 1
					interPort0 = IVPLSRows[i].split("interface ")
					interPort1 = interPort0[1].split(".")
					interPort = interPort1[0]
					#crt.Dialog.MessageBox(str(interPort))
					if Port1 != interPort:
						Port1 = interPort
					GetINTPort = 0

			IVcRowPr1 = "-"
			for i in range (0, len(IVcRow)):
				if IVcRow[i] == 0:
					IVcRowPr1 = IVcRowPr1 + IVconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			IVcRowPr = "- NO Missing configuration" if IVcRowPr1 == "-" else IVcRowPr1

			if GetINTPort == 1:
				crt.Screen.Send("show vpls mac-table instance VODA-MOB-BITSTREAM | no-more\r")
				crt.Screen.WaitForString("Routing instance : VODA-MOB-BITSTREAM")
				readINTPortST = crt.Screen.ReadString("MAC flags")
				readINTPortrows = readINTPortST.splitlines()
				#readINTPortrows = [item.strip() for item in readINTPortrows]
				for i in range (0, len(readINTPortrows)):
					if ".2050" in readINTPortrows[i]:
						readINTPortrow1 = readINTPortrows[i]
						readINTPortrow2 = readINTPortrow1.split("D")
						readINTPortrow = readINTPortrow2[1].strip()
						Port12 = readINTPortrow.split(".")
						Port1 = Port12[0]
				crt.Screen.WaitForString("EG>")

			crt.Screen.Send("show configuration interfaces " + Port1 + ".2050 | display set\r")
			crt.Screen.WaitForString("EG>")

			IRows = []
			IconfRow = crt.Screen.CurrentRow - 1
			readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
			IRows.append(readIconfRow)

			while readIconfRow.endswith("display set") == False:
				IconfRow = IconfRow - 1
				readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
				IRows.append(readIconfRow)

			crt.Screen.Send("show configuration routing-instances VODA-MOB-BITSTREAM interface " + Port1 + ".2050 | display set\r")
			crt.Screen.WaitForString("EG>")

			IconfRow2 = crt.Screen.CurrentRow - 1
			readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
			IRows.append(readIconfRow2)

			while readIconfRow2.endswith("display set") == False:
				IconfRow2 = IconfRow2 - 1
				readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
				IRows.append(readIconfRow2)

			IconfRow1 = "set interfaces " + Port1 + " unit 2050 encapsulation vlan-vpls"
			IconfRow2 = "set interfaces " + Port1 + " unit 2050 vlan-id-range 2050-2099"
			IconfRow3 = "set routing-instances VODA-MOB-BITSTREAM interface " + Port1 + ".2050"
			IconfRow = [IconfRow1,IconfRow2,IconfRow3]
			IcRow = [0,0,0]
			for i in range (0, len(IRows)):
				if IRows[i] == IconfRow[0]:
					IcRow[0] = 1
				if IRows[i] == IconfRow[1]:
					IcRow[1] = 1
				if IRows[i] == IconfRow[2]:
					IcRow[2] = 1

			IcRowPr1 = "-"
			for i in range (0, len(IcRow)):
				if IcRow[i] == 0:
					IcRowPr1 = IcRowPr1 + IconfRow[i] + "\r"
			#crt.Dialog.MessageBox(cRowPr)
			IcRowPr = "- NO Missing configuration" if IcRowPr1 == "-" else IcRowPr1

			"""
			crt.Screen.Send("show vpls connections instance VODA-VPLS-BITSTREAM | no-more\r")
			crt.Screen.WaitForString("EG>")

			INeigRows = []
			INeigRow = crt.Screen.CurrentRow - 1
			readINeigRow = crt.Screen.Get(INeigRow, 1,INeigRow,400).strip()
			INeigRows.append(readINeigRow)

			while readINeigRow.endswith("VODA-VPLS-BITSTREAM") == False:
				INeigRow = INeigRow - 1
				readINeigRow = crt.Screen.Get(INeigRow, 1,INeigRow,400).strip()
				INeigRows.append(readINeigRow)

			for i in range (0, len(INeigRows)):
				if INeigRows[i].startswith(MXRouterIP):
					Ivplsconnrow = INeigRows[i]
					#crt.Dialog.MessageBox(str(vplsconnrow))
			"""
			crt.Screen.Send("show vpls connections instance VODA-MOB-BITSTREAM | no-more\r")
			crt.Screen.WaitForString("VODA-MOB-BITSTREAM")
			OVBRead = crt.Screen.ReadString("EG>")

			INeigRows = OVBRead.splitlines()
			INeigRows = [item.strip() for item in INeigRows]

			for i in range (0, len(INeigRows)):
				if MXRouterIP + "(" in INeigRows[i]:
					Ivplsconnrow = INeigRows[i]
					#crt.Dialog.MessageBox(str(vplsconnrow))


			INTMACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 2050 and int(VlanNum) <= 2099:
						
					crt.Screen.Send("show vpls mac-table instance VODA-MOB-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if "lsi" in VLANRows[j]:
							INTMACs.append("There is MAC from MX Router side [customer] for VLAN " + VlanNum)

						if Port1 +".2050" in VLANRows[j]:
							INTMACs.append("There is MAC from VODAFONE side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					INTMACs.append(addVlan)

			IMACsPr1 = "-"
			INTMACs = list(dict.fromkeys(INTMACs))
			for i in range (0, len(INTMACs)):
				IMACsPr1 = IMACsPr1 + INTMACs[i] + "\r"

			IMACsPr = "- NO MACs received from both side" if IMACsPr1 == "-" else IMACsPr1

			crt.Screen.Send("show interfaces " + Port1 + " | no-more\r")
			crt.Screen.WaitForString("Physical link is")
			InterPortStatus = str(crt.Screen.ReadString("Interface index")).strip()

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match last \r")
			crt.Screen.WaitForString("(")
			InterPortLastFlap = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match rate \r")
			crt.Screen.WaitForString("Input rate")
			InterPortInputRate = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("Output rate")
			InterPortOutputRate = crt.Screen.ReadString(")")


			crt.Dialog.MessageBox("            *****VODA-MOB-BITSTREAM*****\r\r* MX Router : " + AggRouter + "\r\r* MX Port : " + link + "\r\r* Status : UP\r\r* Checking MX Port configuration :\r" + cRowPr + "\r\r* Checking MX VPLS configuration :\r" + VcRowPr + "\r\r* vpls connections Status on MX :\r" + vplsconnrow + "\r\r* MACs on MX : \r" + MACsPr + "\r\r* Interconnection Router : "+ InterRouter + "\r\r* Interconnection Port : " + Port1 + "\r\r* Status : " + InterPortStatus + "\r\r* Last Flap : " + InterPortLastFlap + "\r\r* Input Rate" + InterPortInputRate + ")\r* Output Rate" + InterPortOutputRate + ")\r\r* Checking Interconnection Port configuration :\r" + IcRowPr + "\r\r* Checking Interconnection VPLS configuration :\r" + IVcRowPr + "\r\r* vpls connections Status on Interconnection :\r" + Ivplsconnrow + "\r\r* MACs on Interconnection : \r" + IMACsPr ,"Ahmed Elaraby", BUTTON_CANCEL + ICON_INFO)



#######################################################################################################    
########################################### NOOR ######################################################
#######################################################################################################

def NOOR(user,pass1,link,AggRouter,InterRouter,Port1,Port2):
	crt.Screen.Send("show interfaces descriptions | match " + link + ".2800\r")
	crt.Screen.WaitForString("EG>")

	StatusRows = []
	PortRow = crt.Screen.CurrentRow - 1
	readPortRow1 = crt.Screen.Get(PortRow, 1,PortRow,200).strip()
	StatusRows.append(readPortRow1)

	while readPortRow1.endswith("2800") == False:
		PortRow = PortRow - 1
		readPortRow1 = crt.Screen.Get(PortRow, 1,PortRow,400).strip()
		StatusRows.append(readPortRow1)

	for i in range (0, len(StatusRows)):
		if StatusRows[i].startswith(link):
			readPortRow = StatusRows[i]

	if "up    down" in readPortRow :
		#crt.Dialog.MessageBox("up    down")
		crt.Screen.Send("clear vpls mac-move-action interface " + link + ".2800\r")
		crt.Dialog.MessageBox("check now as mac-move-action cleared")
		return 0
	if "down  up" in readPortRow :
		crt.Dialog.MessageBox("check port is disabled")
		return 0

	if "up    up" in readPortRow :
		#crt.Dialog.MessageBox("up    up")
		crt.Screen.Send("show configuration interfaces " + link + ".2800 | display set\r")
		crt.Screen.WaitForString("EG>")

		Rows = []
		confRow = crt.Screen.CurrentRow - 1
		readconfRow = crt.Screen.Get(confRow, 1,confRow,400).strip()
		Rows.append(readconfRow)

		while readconfRow.endswith("display set") == False:
			confRow = confRow - 1
			readconfRow = crt.Screen.Get(confRow, 1,confRow,400).strip()
			Rows.append(readconfRow)

		crt.Screen.Send("show configuration routing-instances NOOR-VPLS-BITSTREAM interface " + link + ".2800 | display set\r")
		crt.Screen.WaitForString("EG>")

		confRow2 = crt.Screen.CurrentRow - 1
		readconfRow2 = crt.Screen.Get(confRow2, 1,confRow2,400).strip()
		Rows.append(readconfRow2)

		while readconfRow2.endswith("display set") == False:
			confRow2 = confRow2 - 1
			readconfRow2 = crt.Screen.Get(confRow2, 1,confRow2,400).strip()
			Rows.append(readconfRow2)


		confRow1 = "set interfaces " + link + " unit 2800 encapsulation vlan-vpls"
		confRow2 = "set interfaces " + link + " unit 2800 vlan-id-range 2800-3049"
		confRow3 = "set routing-instances NOOR-VPLS-BITSTREAM interface " + link + ".2800"
		confRow = [confRow1,confRow2,confRow3]
		cRow = [0,0,0]
		for i in range (0, len(Rows)):
			if Rows[i] == confRow[0]:
				cRow[0] = 1
			if Rows[i] == confRow[1]:
				cRow[1] = 1
			if Rows[i] == confRow[2]:
				cRow[2] = 1

		cRowPr1 = "-"
		for i in range (0, len(cRow)):
			if cRow[i] == 0:
				cRowPr1 = cRowPr1 + confRow[i] + "\r"
		#crt.Dialog.MessageBox(cRowPr)
		cRowPr = "- NO Missing configuration" if cRowPr1 == "-" else cRowPr1


		if AggRouter == InterRouter :

			if Port2 != "@" :
				crt.Screen.Send("show interfaces " + Port1 + " terse\r")
				#crt.Screen.WaitForString("--> ")
				WaPo = crt.Screen.WaitForStrings(['--> ','vpls','EG>'],5)
				if WaPo == 1:
					Port1 = crt.Screen.ReadString(".")
					GetINTPort = 0
				if WaPo == 2:
					GetINTPort = 1
				if WaPo == 3:
					crt.Screen.Send("\r")
					GetINTPort = 1
				crt.Screen.WaitForString("EG>")

			crt.Screen.Send('show configuration routing-instances NOOR-VPLS-BITSTREAM | except "NOOR-VPLS-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			VPLSRows = []
			VconfRow = crt.Screen.CurrentRow - 1
			readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
			VPLSRows.append(readVconfRow)

			while readVconfRow.endswith("display set") == False:
				VconfRow = VconfRow - 1
				readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
				VPLSRows.append(readVconfRow)

			VconfRow1 = "set routing-instances NOOR-VPLS-BITSTREAM protocols vpls enable-mac-move-action"
			VconfRow2 = "set routing-instances NOOR-VPLS-BITSTREAM protocols vpls mac-table-size 2000"
			VconfRow3 = "set routing-instances NOOR-VPLS-BITSTREAM protocols vpls no-tunnel-services"
			VconfRow4 = "set routing-instances NOOR-VPLS-BITSTREAM protocols vpls vpls-id 2800"
			VconfRow5 = "set routing-instances NOOR-VPLS-BITSTREAM instance-type vpls"
			VconfRow6 = "set routing-instances NOOR-VPLS-BITSTREAM vlan-id all"
			VconfRow7 = "set routing-instances NOOR-VPLS-BITSTREAM protocols vpls interface"

			VconfRow = [VconfRow1 , VconfRow2 , VconfRow3 , VconfRow4 , VconfRow5 , VconfRow6 , VconfRow7]

			VcRow = [0,0,0,0,0,0,0]
			for i in range (0, len(VPLSRows)):
				if VPLSRows[i] == VconfRow[0]:
					VcRow[0] = 1
				if VPLSRows[i] == VconfRow[1]:
					VcRow[1] = 1
				if VPLSRows[i] == VconfRow[2]:
					VcRow[2] = 1
				if VPLSRows[i] == VconfRow[3]:
					VcRow[3] = 1
				if VPLSRows[i] == VconfRow[4]:
					VcRow[4] = 1
				if VPLSRows[i] == VconfRow[5]:
					VcRow[5] = 1
				if VPLSRows[i].startswith(VconfRow[6]) == True:
					VcRow[6] = 1
					interPort0 = VPLSRows[i].split("interface ")
					interPort1 = interPort0[1].split(".")
					interPort = interPort1[0]
					#crt.Dialog.MessageBox(str(interPort))
					if Port1 != interPort:
						Port1 = interPort
					GetINTPort = 0

			VcRowPr1 = "-"
			for i in range (0, len(VcRow)):
				if VcRow[i] == 0:
					VcRowPr1 = VcRowPr1 + VconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			VcRowPr = "- NO Missing configuration" if VcRowPr1 == "-" else VcRowPr1

			if GetINTPort == 1:
				crt.Screen.Send("show vpls mac-table instance NOOR-VPLS-BITSTREAM | no-more\r")
				crt.Screen.WaitForString("Routing instance : NOOR-VPLS-BITSTREAM")
				readINTPortST = crt.Screen.ReadString("MAC flags")
				readINTPortrows = readINTPortST.splitlines()
				#readINTPortrows = [item.strip() for item in readINTPortrows]
				for i in range (0, len(readINTPortrows)):
					if ".2800" in readINTPortrows[i]:
						readINTPortrow1 = readINTPortrows[i]
						readINTPortrow2 = readINTPortrow1.split("D")
						readINTPortrow = readINTPortrow2[1].strip()
						Port12 = readINTPortrow.split(".")
						Port1 = Port12[0]
				crt.Screen.WaitForString("EG>")

			crt.Screen.Send("show configuration interfaces " + Port1 + ".2800 | display set\r")
			crt.Screen.WaitForString("EG>")

			IRows = []
			IconfRow = crt.Screen.CurrentRow - 1
			readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
			IRows.append(readIconfRow)

			while readIconfRow.endswith("display set") == False:
				IconfRow = IconfRow - 1
				readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
				IRows.append(readIconfRow)

			crt.Screen.Send("show configuration routing-instances NOOR-VPLS-BITSTREAM interface " + Port1 + ".2800 | display set\r")
			crt.Screen.WaitForString("EG>")

			IconfRow2 = crt.Screen.CurrentRow - 1
			readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
			IRows.append(readIconfRow2)

			while readIconfRow2.endswith("display set") == False:
				IconfRow2 = IconfRow2 - 1
				readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
				IRows.append(readIconfRow2)

			IconfRow1 = "set interfaces " + Port1 + " unit 2800 encapsulation vlan-vpls"
			IconfRow2 = "set interfaces " + Port1 + " unit 2800 vlan-id-range 2800-3049"
			IconfRow3 = "set routing-instances NOOR-VPLS-BITSTREAM interface " + Port1 + ".2800"
			IconfRow = [IconfRow1,IconfRow2,IconfRow3]
			IcRow = [0,0,0]
			for i in range (0, len(IRows)):
				if IRows[i] == IconfRow[0]:
					IcRow[0] = 1
				if IRows[i] == IconfRow[1]:
					IcRow[1] = 1
				if IRows[i] == IconfRow[2]:
					IcRow[2] = 1

			IcRowPr1 = "-"
			for i in range (0, len(IcRow)):
				if IcRow[i] == 0:
					IcRowPr1 = IcRowPr1 + IconfRow[i] + "\r"
			#crt.Dialog.MessageBox(cRowPr)
			IcRowPr = "- NO Missing configuration" if IcRowPr1 == "-" else IcRowPr1


			vlanNums = crt.Dialog.Prompt("Please Enter affected VLANs seperating with space :","Ahmed Elaraby")
			VLANs = vlanNums.split()
			MACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 2800 and int(VlanNum) <= 3049:
						
					crt.Screen.Send("show vpls mac-table instance NOOR-VPLS-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if Port1 + ".2800" in VLANRows[j]:
							MACs.append("There is MAC from NOOR side for VLAN " + VlanNum)

						if link +".2800" in VLANRows[j]:
							MACs.append("There is MAC from Customer side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					MACs.append(addVlan)

			MACsPr1 = "-"
			MACs = list(dict.fromkeys(MACs))
			for i in range (0, len(MACs)):
				MACsPr1 = MACsPr1 + MACs[i] + "\r"

			MACsPr = "- NO MACs received from both side" if MACsPr1 == "-" else MACsPr1

			crt.Screen.Send("show interfaces " + Port1 + " | no-more\r")
			crt.Screen.WaitForString("Physical link is")
			InterPortStatus = str(crt.Screen.ReadString("Interface index")).strip()

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match last \r")
			crt.Screen.WaitForString("(")
			InterPortLastFlap = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match rate \r")
			crt.Screen.WaitForString("Input rate")
			InterPortInputRate = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("Output rate")
			InterPortOutputRate = crt.Screen.ReadString(")")




			crt.Dialog.MessageBox("            *****NOOR-VPLS-BITSTREAM*****\r\r* MX Router : " + AggRouter + "\r\r* MX Port : " + link + "\r\r* Status : UP\r\r* Checking MX Port configuration :\r" + cRowPr +  "\r\r* Checking VPLS configuration :\r" + VcRowPr + "\r\r* Interconnection Router : "+ InterRouter + "\r\r* Interconnection Port : " + Port1 + "\r\r* Status : " + InterPortStatus + "\r\r* Last Flap : " + InterPortLastFlap + "\r\r* Input Rate" + InterPortInputRate + ")\r* Output Rate" + InterPortOutputRate + ")\r\r* MACs : \r" + MACsPr ,"Ahmed Elaraby", BUTTON_CANCEL + ICON_INFO)



		if AggRouter != InterRouter :
			#crt.Dialog.MessageBox("AggRouter != InterRouter")
			crt.Screen.Send('show configuration routing-instances NOOR-VPLS-BITSTREAM | except "NOOR-VPLS-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			VPLSRows = []
			VconfRow = crt.Screen.CurrentRow - 1
			readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
			VPLSRows.append(readVconfRow)

			while readVconfRow.endswith("display set") == False:
				VconfRow = VconfRow - 1
				readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
				VPLSRows.append(readVconfRow)

			VconfRow1 = "set routing-instances NOOR-VPLS-BITSTREAM protocols vpls enable-mac-move-action"
			VconfRow2 = "set routing-instances NOOR-VPLS-BITSTREAM protocols vpls mac-table-size 2000"
			VconfRow3 = "set routing-instances NOOR-VPLS-BITSTREAM protocols vpls no-tunnel-services"
			VconfRow4 = "set routing-instances NOOR-VPLS-BITSTREAM protocols vpls vpls-id 2800"
			VconfRow5 = "set routing-instances NOOR-VPLS-BITSTREAM instance-type vpls"
			VconfRow6 = "set routing-instances NOOR-VPLS-BITSTREAM vlan-id all"
			VconfRow7 = "set routing-instances NOOR-VPLS-BITSTREAM protocols vpls neighbor"

			VconfRow = [VconfRow1 , VconfRow2 , VconfRow3 , VconfRow4 , VconfRow5 , VconfRow6 , VconfRow7]

			VcRow = [0,0,0,0,0,0,0]
			neigIP = "@"
			for i in range (0, len(VPLSRows)):
				if VPLSRows[i] == VconfRow[0]:
					VcRow[0] = 1
				if VPLSRows[i] == VconfRow[1]:
					VcRow[1] = 1
				if VPLSRows[i] == VconfRow[2]:
					VcRow[2] = 1
				if VPLSRows[i] == VconfRow[3]:
					VcRow[3] = 1
				if VPLSRows[i] == VconfRow[4]:
					VcRow[4] = 1
				if VPLSRows[i] == VconfRow[5]:
					VcRow[5] = 1
				if VPLSRows[i].startswith(VconfRow[6]) == True:
					VcRow[6] = 1
					neigIP0 = VPLSRows[i].split("neighbor ")
					neigIP1 = neigIP0[1].split(" ")
					neigIP = neigIP1[0]

			"""
			if neigIP == "@":

				data =[]
				FileName = "Devices.csv"
				try:
					with open(os.path.join(os.path.dirname(__file__), FileName), mode='r') as csvfile:
						reader = csv.reader(csvfile)
						for row in reader:
							data.append(row)
				except EnvironmentError:
					crt.Dialog.MessageBox("Sorry Can't Open File! Please Change Files and Script Location!","Ahmed Elaraby")
					return 0

				TARGETCICol = [x[11] for x in data]
				if InterRouter in TARGETCICol:
					for x in range(0,len(data)):
						if InterRouter == data[x][11]:
							neigIP = data[x][5]

			"""

			VcRowPr1 = "-"
			for i in range (0, len(VcRow)):
				if VcRow[i] == 0:
					VcRowPr1 = VcRowPr1 + VconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			VcRowPr = "- NO Missing configuration" if VcRowPr1 == "-" else VcRowPr1

			crt.Screen.Send("show vpls connections instance NOOR-VPLS-BITSTREAM | no-more\r")
			crt.Screen.WaitForString("EG>")

			NeigRows = []
			NeigRow = crt.Screen.CurrentRow - 1
			readNeigRow = crt.Screen.Get(NeigRow, 1,NeigRow,400).strip()
			NeigRows.append(readNeigRow)

			while readNeigRow.endswith("NOOR-VPLS-BITSTREAM") == False:
				NeigRow = NeigRow - 1
				readNeigRow = crt.Screen.Get(NeigRow, 1,NeigRow,400).strip()
				NeigRows.append(readNeigRow)

			for i in range (0, len(NeigRows)):
				if NeigRows[i].startswith(neigIP):
					vplsconnrow = NeigRows[i]
					#crt.Dialog.MessageBox(str(vplsconnrow))


			vlanNums = crt.Dialog.Prompt("Please Enter affected VLANs seperating with space :","Ahmed Elaraby")
			VLANs = vlanNums.split()
			MXMACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 2800 and int(VlanNum) <= 3049:
						
					crt.Screen.Send("show vpls mac-table instance NOOR-VPLS-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if "lsi" in VLANRows[j]:
							MXMACs.append("There is MAC from Interconnection side [NOOR] for VLAN " + VlanNum)

						if link +".2800" in VLANRows[j]:
							MXMACs.append("There is MAC from Customer side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					MXMACs.append(addVlan)

			MACsPr1 = "-"
			MXMACs = list(dict.fromkeys(MXMACs))
			for i in range (0, len(MXMACs)):
				MACsPr1 = MACsPr1 + MXMACs[i] + "\r"

			MACsPr = "- NO MACs received from both side" if MACsPr1 == "-" else MACsPr1

			crt.Screen.Send("show interfaces lo0.0\r")
			crt.Screen.WaitForString("Local: ")
			MXRouterIP = crt.Screen.ReadString("\r").strip()
			#crt.Dialog.MessageBox(MXRouterIP)

			crt.Screen.Send("quit\r")
			crt.Screen.WaitForString("~]$")

			if neigIP == "@":
				crt.Screen.Send("alias " + InterRouter + "\r")
				crt.Screen.WaitForString("telnet")
				neigIP = crt.Screen.ReadString("'").strip()
				crt.Screen.WaitForString("~]$")

			crt.Screen.Send("telnet " + neigIP + "\r")
			crt.Screen.WaitForString("login:")
			crt.Screen.Send(user+"\r")
			crt.Screen.WaitForString("Password:")
			crt.Screen.Send(pass1+"\r")
			crt.Screen.WaitForString("EG>")

			if Port2 != "@" :
				crt.Screen.Send("show interfaces " + Port1 + " terse\r")
				#crt.Screen.WaitForString("--> ")
				WaPo = crt.Screen.WaitForStrings(['--> ','vpls','EG>'],5)
				if WaPo == 1:
					Port1 = crt.Screen.ReadString(".")
					GetINTPort = 0
				if WaPo == 2:
					GetINTPort = 1
				if WaPo == 3:
					crt.Screen.Send("\r")
					GetINTPort = 1
				crt.Screen.WaitForString("EG>")


			crt.Screen.Send('show configuration routing-instances NOOR-VPLS-BITSTREAM | except "NOOR-VPLS-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			IVPLSRows = []
			IVconfRow = crt.Screen.CurrentRow - 1
			readIVconfRow = crt.Screen.Get(IVconfRow, 1,IVconfRow,400).strip()
			IVPLSRows.append(readIVconfRow)

			while readIVconfRow.endswith("display set") == False:
				IVconfRow = IVconfRow - 1
				readIVconfRow = crt.Screen.Get(IVconfRow, 1,IVconfRow,400).strip()
				IVPLSRows.append(readIVconfRow)

			IVconfRow1 = "set routing-instances NOOR-VPLS-BITSTREAM protocols vpls enable-mac-move-action"
			IVconfRow2 = "set routing-instances NOOR-VPLS-BITSTREAM protocols vpls mac-table-size 2000"
			IVconfRow3 = "set routing-instances NOOR-VPLS-BITSTREAM protocols vpls no-tunnel-services"
			IVconfRow4 = "set routing-instances NOOR-VPLS-BITSTREAM protocols vpls vpls-id 2800"
			IVconfRow5 = "set routing-instances NOOR-VPLS-BITSTREAM instance-type vpls"
			IVconfRow6 = "set routing-instances NOOR-VPLS-BITSTREAM vlan-id all"
			IVconfRow7 = "set routing-instances NOOR-VPLS-BITSTREAM protocols vpls interface"

			IVconfRow = [IVconfRow1 , IVconfRow2 , IVconfRow3 , IVconfRow4 , IVconfRow5 , IVconfRow6 , IVconfRow7]

			IVcRow = [0,0,0,0,0,0,0]
			for i in range (0, len(IVPLSRows)):
				if IVPLSRows[i] == IVconfRow[0]:
					IVcRow[0] = 1
				if IVPLSRows[i] == IVconfRow[1]:
					IVcRow[1] = 1
				if IVPLSRows[i] == IVconfRow[2]:
					IVcRow[2] = 1
				if IVPLSRows[i] == IVconfRow[3]:
					IVcRow[3] = 1
				if IVPLSRows[i] == IVconfRow[4]:
					IVcRow[4] = 1
				if IVPLSRows[i] == IVconfRow[5]:
					IVcRow[5] = 1
				if IVPLSRows[i].startswith(IVconfRow[6]) == True:
					IVcRow[6] = 1
					interPort0 = IVPLSRows[i].split("interface ")
					interPort1 = interPort0[1].split(".")
					interPort = interPort1[0]
					#crt.Dialog.MessageBox(str(interPort))
					if Port1 != interPort:
						Port1 = interPort
					GetINTPort = 0

			IVcRowPr1 = "-"
			for i in range (0, len(IVcRow)):
				if IVcRow[i] == 0:
					IVcRowPr1 = IVcRowPr1 + IVconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			IVcRowPr = "- NO Missing configuration" if IVcRowPr1 == "-" else IVcRowPr1

			if GetINTPort == 1:
				crt.Screen.Send("show vpls mac-table instance NOOR-VPLS-BITSTREAM | no-more\r")
				crt.Screen.WaitForString("Routing instance : NOOR-VPLS-BITSTREAM")
				readINTPortST = crt.Screen.ReadString("MAC flags")
				readINTPortrows = readINTPortST.splitlines()
				#readINTPortrows = [item.strip() for item in readINTPortrows]
				for i in range (0, len(readINTPortrows)):
					if ".2800" in readINTPortrows[i]:
						readINTPortrow1 = readINTPortrows[i]
						readINTPortrow2 = readINTPortrow1.split("D")
						readINTPortrow = readINTPortrow2[1].strip()
						Port12 = readINTPortrow.split(".")
						Port1 = Port12[0]
				crt.Screen.WaitForString("EG>")

			crt.Screen.Send("show configuration interfaces " + Port1 + ".2800 | display set\r")
			crt.Screen.WaitForString("EG>")

			IRows = []
			IconfRow = crt.Screen.CurrentRow - 1
			readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
			IRows.append(readIconfRow)

			while readIconfRow.endswith("display set") == False:
				IconfRow = IconfRow - 1
				readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
				IRows.append(readIconfRow)

			crt.Screen.Send("show configuration routing-instances NOOR-VPLS-BITSTREAM interface " + Port1 + ".2800 | display set\r")
			crt.Screen.WaitForString("EG>")

			IconfRow2 = crt.Screen.CurrentRow - 1
			readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
			IRows.append(readIconfRow2)

			while readIconfRow2.endswith("display set") == False:
				IconfRow2 = IconfRow2 - 1
				readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
				IRows.append(readIconfRow2)

			IconfRow1 = "set interfaces " + Port1 + " unit 2800 encapsulation vlan-vpls"
			IconfRow2 = "set interfaces " + Port1 + " unit 2800 vlan-id-range 2800-3049"
			IconfRow3 = "set routing-instances NOOR-VPLS-BITSTREAM interface " + Port1 + ".2800"
			IconfRow = [IconfRow1,IconfRow2,IconfRow3]
			IcRow = [0,0,0]
			for i in range (0, len(IRows)):
				if IRows[i] == IconfRow[0]:
					IcRow[0] = 1
				if IRows[i] == IconfRow[1]:
					IcRow[1] = 1
				if IRows[i] == IconfRow[2]:
					IcRow[2] = 1

			IcRowPr1 = "-"
			for i in range (0, len(IcRow)):
				if IcRow[i] == 0:
					IcRowPr1 = IcRowPr1 + IconfRow[i] + "\r"
			#crt.Dialog.MessageBox(cRowPr)
			IcRowPr = "- NO Missing configuration" if IcRowPr1 == "-" else IcRowPr1

			crt.Screen.Send("show vpls connections instance NOOR-VPLS-BITSTREAM | no-more\r")
			crt.Screen.WaitForString("NOOR-VPLS-BITSTREAM")
			OVBRead = crt.Screen.ReadString("EG>")


			INeigRows = OVBRead.splitlines()
			INeigRows = [item.strip() for item in INeigRows]

			"""
			INeigRow = crt.Screen.CurrentRow - 1
			readINeigRow = crt.Screen.Get(INeigRow, 1,INeigRow,400).strip()
			INeigRows.append(readINeigRow)

			while readINeigRow.endswith("ORANGE-VPLS-BITSTREAM") == False:
				INeigRow = INeigRow - 1
				readINeigRow = crt.Screen.Get(INeigRow, 1,INeigRow,400).strip()
				INeigRows.append(readINeigRow)
			"""
			for i in range (0, len(INeigRows)):
				if MXRouterIP + "(" in INeigRows[i]:
					Ivplsconnrow = INeigRows[i]
					#crt.Dialog.MessageBox(str(vplsconnrow))

			INTMACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 2800 and int(VlanNum) <= 3049:
						
					crt.Screen.Send("show vpls mac-table instance NOOR-VPLS-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if "lsi" in VLANRows[j]:
							INTMACs.append("There is MAC from MX Router side [customer] for VLAN " + VlanNum)

						if Port1 +".2800" in VLANRows[j]:
							INTMACs.append("There is MAC from NOOR side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					INTMACs.append(addVlan)

			IMACsPr1 = "-"
			INTMACs = list(dict.fromkeys(INTMACs))
			for i in range (0, len(INTMACs)):
				IMACsPr1 = IMACsPr1 + INTMACs[i] + "\r"

			IMACsPr = "- NO MACs received from both side" if IMACsPr1 == "-" else IMACsPr1

			crt.Screen.Send("show interfaces " + Port1 + " | no-more\r")
			crt.Screen.WaitForString("Physical link is")
			InterPortStatus = str(crt.Screen.ReadString("Interface index")).strip()

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match last \r")
			crt.Screen.WaitForString("(")
			InterPortLastFlap = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match rate \r")
			crt.Screen.WaitForString("Input rate")
			InterPortInputRate = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("Output rate")
			InterPortOutputRate = crt.Screen.ReadString(")")


			crt.Dialog.MessageBox("            *****NOOR-VPLS-BITSTREAM*****\r\r* MX Router : " + AggRouter + "\r\r* MX Port : " + link + "\r\r* Status : UP\r\r* Checking MX Port configuration :\r" + cRowPr + "\r\r* Checking MX VPLS configuration :\r" + VcRowPr + "\r\r* vpls connections Status on MX :\r" + vplsconnrow + "\r\r* MACs on MX : \r" + MACsPr + "\r\r* Interconnection Router : "+ InterRouter + "\r\r* Interconnection Port : " + Port1 + "\r\r* Status : " + InterPortStatus + "\r\r* Last Flap : " + InterPortLastFlap + "\r\r* Input Rate" + InterPortInputRate + ")\r* Output Rate" + InterPortOutputRate + ")\r\r* Checking Interconnection Port configuration :\r" + IcRowPr + "\r\r* Checking Interconnection VPLS configuration :\r" + IVcRowPr + "\r\r* vpls connections Status on Interconnection :\r" + Ivplsconnrow + "\r\r* MACs on Interconnection : \r" + IMACsPr ,"Ahmed Elaraby", BUTTON_CANCEL + ICON_INFO)



#######################################################################################################    
########################################### ORANGE ####################################################
#######################################################################################################

def ORANGE(user,pass1,link,AggRouter,InterRouter,Port1,Port2):
	crt.Screen.Send("show interfaces descriptions | match " + link + ".3050\r")
	crt.Screen.WaitForString("EG>")

	StatusRows = []
	PortRow = crt.Screen.CurrentRow - 1
	readPortRow1 = crt.Screen.Get(PortRow, 1,PortRow,200).strip()
	StatusRows.append(readPortRow1)

	while readPortRow1.endswith("3050") == False:
		PortRow = PortRow - 1
		readPortRow1 = crt.Screen.Get(PortRow, 1,PortRow,400).strip()
		StatusRows.append(readPortRow1)

	for i in range (0, len(StatusRows)):
		if StatusRows[i].startswith(link):
			readPortRow = StatusRows[i]


	if "up    down" in readPortRow :
		#crt.Dialog.MessageBox("up    down")
		crt.Screen.Send("clear vpls mac-move-action interface " + link + ".3050\r")
		crt.Dialog.MessageBox("check now as mac-move-action cleared")
		return 0
	if "down  up" in readPortRow :
		crt.Dialog.MessageBox("check port is disabled")
		return 0

	if "up    up" in readPortRow :
		#crt.Dialog.MessageBox("up    up")
		crt.Screen.Send("show configuration interfaces " + link + ".3050 | display set\r")
		crt.Screen.WaitForString("EG>")

		Rows = []
		confRow = crt.Screen.CurrentRow - 1
		readconfRow = crt.Screen.Get(confRow, 1,confRow,400).strip()
		Rows.append(readconfRow)

		while readconfRow.endswith("display set") == False:
			confRow = confRow - 1
			readconfRow = crt.Screen.Get(confRow, 1,confRow,400).strip()
			Rows.append(readconfRow)

		crt.Screen.Send("show configuration routing-instances ORANGE-VPLS-BITSTREAM interface " + link + ".3050 | display set\r")
		crt.Screen.WaitForString("EG>")

		confRow2 = crt.Screen.CurrentRow - 1
		readconfRow2 = crt.Screen.Get(confRow2, 1,confRow2,400).strip()
		Rows.append(readconfRow2)

		while readconfRow2.endswith("display set") == False:
			confRow2 = confRow2 - 1
			readconfRow2 = crt.Screen.Get(confRow2, 1,confRow2,400).strip()
			Rows.append(readconfRow2)


		confRow1 = "set interfaces " + link + " unit 3050 encapsulation vlan-vpls"
		confRow2 = "set interfaces " + link + " unit 3050 vlan-id-range 3050-3299"
		confRow3 = "set routing-instances ORANGE-VPLS-BITSTREAM interface " + link + ".3050"
		confRow = [confRow1,confRow2,confRow3]
		cRow = [0,0,0]
		for i in range (0, len(Rows)):
			if Rows[i] == confRow[0]:
				cRow[0] = 1
			if Rows[i] == confRow[1]:
				cRow[1] = 1
			if Rows[i] == confRow[2]:
				cRow[2] = 1

		cRowPr1 = "-"
		for i in range (0, len(cRow)):
			if cRow[i] == 0:
				cRowPr1 = cRowPr1 + confRow[i] + "\r"
		#crt.Dialog.MessageBox(cRowPr)
		cRowPr = "- NO Missing configuration" if cRowPr1 == "-" else cRowPr1


		if AggRouter == InterRouter :

			if Port2 != "@" :
				crt.Screen.Send("show interfaces " + Port1 + " terse\r")
				#crt.Screen.WaitForString("--> ")
				WaPo = crt.Screen.WaitForStrings(['--> ','vpls','EG>'],5)
				if WaPo == 1:
					Port1 = crt.Screen.ReadString(".")
					GetINTPort = 0
				if WaPo == 2:
					GetINTPort = 1
				if WaPo == 3:
					crt.Screen.Send("\r")
					GetINTPort = 1
				crt.Screen.WaitForString("EG>")

			crt.Screen.Send('show configuration routing-instances ORANGE-VPLS-BITSTREAM | except "ORANGE-VPLS-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			VPLSRows = []
			VconfRow = crt.Screen.CurrentRow - 1
			readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
			VPLSRows.append(readVconfRow)

			while readVconfRow.endswith("display set") == False:
				VconfRow = VconfRow - 1
				readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
				VPLSRows.append(readVconfRow)

			VconfRow1 = "set routing-instances ORANGE-VPLS-BITSTREAM protocols vpls enable-mac-move-action"
			VconfRow2 = "set routing-instances ORANGE-VPLS-BITSTREAM protocols vpls mac-table-size 2000"
			VconfRow3 = "set routing-instances ORANGE-VPLS-BITSTREAM protocols vpls no-tunnel-services"
			VconfRow4 = "set routing-instances ORANGE-VPLS-BITSTREAM protocols vpls vpls-id 3050"
			VconfRow5 = "set routing-instances ORANGE-VPLS-BITSTREAM instance-type vpls"
			VconfRow6 = "set routing-instances ORANGE-VPLS-BITSTREAM vlan-id all"
			VconfRow7 = "set routing-instances ORANGE-VPLS-BITSTREAM protocols vpls interface"

			VconfRow = [VconfRow1 , VconfRow2 , VconfRow3 , VconfRow4 , VconfRow5 , VconfRow6 , VconfRow7]

			VcRow = [0,0,0,0,0,0,0]
			for i in range (0, len(VPLSRows)):
				if VPLSRows[i] == VconfRow[0]:
					VcRow[0] = 1
				if VPLSRows[i] == VconfRow[1]:
					VcRow[1] = 1
				if VPLSRows[i] == VconfRow[2]:
					VcRow[2] = 1
				if VPLSRows[i] == VconfRow[3]:
					VcRow[3] = 1
				if VPLSRows[i] == VconfRow[4]:
					VcRow[4] = 1
				if VPLSRows[i] == VconfRow[5]:
					VcRow[5] = 1
				if VPLSRows[i].startswith(VconfRow[6]) == True:
					VcRow[6] = 1
					interPort0 = VPLSRows[i].split("interface ")
					interPort1 = interPort0[1].split(".")
					interPort = interPort1[0]
					#crt.Dialog.MessageBox(str(interPort))
					if Port1 != interPort:
						Port1 = interPort
					GetINTPort = 0

			VcRowPr1 = "-"
			for i in range (0, len(VcRow)):
				if VcRow[i] == 0:
					VcRowPr1 = VcRowPr1 + VconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			VcRowPr = "- NO Missing configuration" if VcRowPr1 == "-" else VcRowPr1

			if GetINTPort == 1:
				crt.Screen.Send("show vpls mac-table instance ORANGE-VPLS-BITSTREAM | no-more\r")
				crt.Screen.WaitForString("Routing instance : ORANGE-VPLS-BITSTREAM")
				readINTPortST = crt.Screen.ReadString("MAC flags")
				readINTPortrows = readINTPortST.splitlines()
				#readINTPortrows = [item.strip() for item in readINTPortrows]
				for i in range (0, len(readINTPortrows)):
					if ".3050" in readINTPortrows[i]:
						readINTPortrow1 = readINTPortrows[i]
						readINTPortrow2 = readINTPortrow1.split("D")
						readINTPortrow = readINTPortrow2[1].strip()
						Port12 = readINTPortrow.split(".")
						Port1 = Port12[0]
				crt.Screen.WaitForString("EG>")


			crt.Screen.Send("show configuration interfaces " + Port1 + ".3050 | display set\r")
			crt.Screen.WaitForString("EG>")

			IRows = []
			IconfRow = crt.Screen.CurrentRow - 1
			readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
			IRows.append(readIconfRow)

			while readIconfRow.endswith("display set") == False:
				IconfRow = IconfRow - 1
				readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
				IRows.append(readIconfRow)

			crt.Screen.Send("show configuration routing-instances ORANGE-VPLS-BITSTREAM interface " + Port1 + ".3050 | display set\r")
			crt.Screen.WaitForString("EG>")

			IconfRow2 = crt.Screen.CurrentRow - 1
			readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
			IRows.append(readIconfRow2)

			while readIconfRow2.endswith("display set") == False:
				IconfRow2 = IconfRow2 - 1
				readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
				IRows.append(readIconfRow2)

			IconfRow1 = "set interfaces " + Port1 + " unit 3050 encapsulation vlan-vpls"
			IconfRow2 = "set interfaces " + Port1 + " unit 3050 vlan-id-range 3050-3299"
			IconfRow3 = "set routing-instances ORANGE-VPLS-BITSTREAM interface " + Port1 + ".3050"
			IconfRow = [IconfRow1,IconfRow2,IconfRow3]
			IcRow = [0,0,0]
			for i in range (0, len(IRows)):
				if IRows[i] == IconfRow[0]:
					IcRow[0] = 1
				if IRows[i] == IconfRow[1]:
					IcRow[1] = 1
				if IRows[i] == IconfRow[2]:
					IcRow[2] = 1

			IcRowPr1 = "-"
			for i in range (0, len(IcRow)):
				if IcRow[i] == 0:
					IcRowPr1 = IcRowPr1 + IconfRow[i] + "\r"
			#crt.Dialog.MessageBox(cRowPr)
			IcRowPr = "- NO Missing configuration" if IcRowPr1 == "-" else IcRowPr1


			vlanNums = crt.Dialog.Prompt("Please Enter affected VLANs seperating with space :","Ahmed Elaraby")
			VLANs = vlanNums.split()
			MACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 3050 and int(VlanNum) <= 3299:
						
					crt.Screen.Send("show vpls mac-table instance ORANGE-VPLS-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if Port1 + ".3050" in VLANRows[j]:
							MACs.append("There is MAC from ETISALAT side for VLAN " + VlanNum)

						if link +".3050" in VLANRows[j]:
							MACs.append("There is MAC from Customer side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					MACs.append(addVlan)

			MACsPr1 = "-"
			MACs = list(dict.fromkeys(MACs))
			for i in range (0, len(MACs)):
				MACsPr1 = MACsPr1 + MACs[i] + "\r"

			MACsPr = "- NO MACs received from both side" if MACsPr1 == "-" else MACsPr1

			crt.Screen.Send("show interfaces " + Port1 + " | no-more\r")
			crt.Screen.WaitForString("Physical link is")
			InterPortStatus = str(crt.Screen.ReadString("Interface index")).strip()

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match last \r")
			crt.Screen.WaitForString("(")
			InterPortLastFlap = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match rate \r")
			crt.Screen.WaitForString("Input rate")
			InterPortInputRate = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("Output rate")
			InterPortOutputRate = crt.Screen.ReadString(")")




			crt.Dialog.MessageBox("            *****ORANGE-VPLS-BITSTREAM*****\r\r* MX Router : " + AggRouter + "\r\r* MX Port : " + link + "\r\r* Status : UP\r\r* Checking MX Port configuration :\r" + cRowPr +  "\r\r* Checking VPLS configuration :\r" + VcRowPr + "\r\r* Interconnection Router : "+ InterRouter + "\r\r* Interconnection Port : " + Port1 + "\r\r* Status : " + InterPortStatus + "\r\r* Last Flap : " + InterPortLastFlap + "\r\r* Input Rate" + InterPortInputRate + ")\r* Output Rate" + InterPortOutputRate + ")\r\r* MACs : \r" + MACsPr ,"Ahmed Elaraby", BUTTON_CANCEL + ICON_INFO)



		if AggRouter != InterRouter :
			#crt.Dialog.MessageBox("AggRouter != InterRouter")
			crt.Screen.Send('show configuration routing-instances ORANGE-VPLS-BITSTREAM | except "ORANGE-VPLS-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			VPLSRows = []
			VconfRow = crt.Screen.CurrentRow - 1
			readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
			VPLSRows.append(readVconfRow)

			while readVconfRow.endswith("display set") == False:
				VconfRow = VconfRow - 1
				readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
				VPLSRows.append(readVconfRow)

			VconfRow1 = "set routing-instances ORANGE-VPLS-BITSTREAM protocols vpls enable-mac-move-action"
			VconfRow2 = "set routing-instances ORANGE-VPLS-BITSTREAM protocols vpls mac-table-size 2000"
			VconfRow3 = "set routing-instances ORANGE-VPLS-BITSTREAM protocols vpls no-tunnel-services"
			VconfRow4 = "set routing-instances ORANGE-VPLS-BITSTREAM protocols vpls vpls-id 3050"
			VconfRow5 = "set routing-instances ORANGE-VPLS-BITSTREAM instance-type vpls"
			VconfRow6 = "set routing-instances ORANGE-VPLS-BITSTREAM vlan-id all"
			VconfRow7 = "set routing-instances ORANGE-VPLS-BITSTREAM protocols vpls neighbor"

			VconfRow = [VconfRow1 , VconfRow2 , VconfRow3 , VconfRow4 , VconfRow5 , VconfRow6 , VconfRow7]

			VcRow = [0,0,0,0,0,0,0]
			neigIP = "@"
			for i in range (0, len(VPLSRows)):
				if VPLSRows[i] == VconfRow[0]:
					VcRow[0] = 1
				if VPLSRows[i] == VconfRow[1]:
					VcRow[1] = 1
				if VPLSRows[i] == VconfRow[2]:
					VcRow[2] = 1
				if VPLSRows[i] == VconfRow[3]:
					VcRow[3] = 1
				if VPLSRows[i] == VconfRow[4]:
					VcRow[4] = 1
				if VPLSRows[i] == VconfRow[5]:
					VcRow[5] = 1
				if VPLSRows[i].startswith(VconfRow[6]) == True:
					VcRow[6] = 1
					neigIP0 = VPLSRows[i].split("neighbor ")
					neigIP1 = neigIP0[1].split(" ")
					neigIP = neigIP1[0]

			"""
			if neigIP == "@":

				data =[]
				FileName = "Devices.csv"
				try:
					with open(os.path.join(os.path.dirname(__file__), FileName), mode='r') as csvfile:
						reader = csv.reader(csvfile)
						for row in reader:
							data.append(row)
				except EnvironmentError:
					crt.Dialog.MessageBox("Sorry Can't Open File! Please Change Files and Script Location!","Ahmed Elaraby")
					return 0

				TARGETCICol = [x[11] for x in data]
				if InterRouter in TARGETCICol:
					for x in range(0,len(data)):
						if InterRouter == data[x][11]:
							neigIP = data[x][5]

			"""

			VcRowPr1 = "-"
			for i in range (0, len(VcRow)):
				if VcRow[i] == 0:
					VcRowPr1 = VcRowPr1 + VconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			VcRowPr = "- NO Missing configuration" if VcRowPr1 == "-" else VcRowPr1

			crt.Screen.Send("show vpls connections instance ORANGE-VPLS-BITSTREAM | no-more\r")
			crt.Screen.WaitForString("EG>")

			NeigRows = []
			NeigRow = crt.Screen.CurrentRow - 1
			readNeigRow = crt.Screen.Get(NeigRow, 1,NeigRow,400).strip()
			NeigRows.append(readNeigRow)

			while readNeigRow.endswith("ORANGE-VPLS-BITSTREAM") == False:
				NeigRow = NeigRow - 1
				readNeigRow = crt.Screen.Get(NeigRow, 1,NeigRow,400).strip()
				NeigRows.append(readNeigRow)

			for i in range (0, len(NeigRows)):
				if NeigRows[i].startswith(neigIP):
					vplsconnrow = NeigRows[i]
					#crt.Dialog.MessageBox(str(vplsconnrow))


			vlanNums = crt.Dialog.Prompt("Please Enter affected VLANs seperating with space :","Ahmed Elaraby")
			VLANs = vlanNums.split()
			MXMACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 3050 and int(VlanNum) <= 3299:
						
					crt.Screen.Send("show vpls mac-table instance ORANGE-VPLS-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if "lsi" in VLANRows[j]:
							MXMACs.append("There is MAC from Interconnection side [ORANGE] for VLAN " + VlanNum)

						if link +".3050" in VLANRows[j]:
							MXMACs.append("There is MAC from Customer side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					MXMACs.append(addVlan)

			MACsPr1 = "-"
			MXMACs = list(dict.fromkeys(MXMACs))
			for i in range (0, len(MXMACs)):
				MACsPr1 = MACsPr1 + MXMACs[i] + "\r"

			MACsPr = "- NO MACs received from both side" if MACsPr1 == "-" else MACsPr1

			crt.Screen.Send("show interfaces lo0.0\r")
			crt.Screen.WaitForString("Local: ")
			MXRouterIP = crt.Screen.ReadString("\r").strip()
			#crt.Dialog.MessageBox(MXRouterIP)

			crt.Screen.Send("quit\r")
			crt.Screen.WaitForString("~]$")

			if neigIP == "@":
				crt.Screen.Send("alias " + InterRouter + "\r")
				crt.Screen.WaitForString("telnet")
				neigIP = crt.Screen.ReadString("'").strip()
				crt.Screen.WaitForString("~]$")

			crt.Screen.Send("telnet " + neigIP + "\r")
			crt.Screen.WaitForString("login:")
			crt.Screen.Send(user+"\r")
			crt.Screen.WaitForString("Password:")
			crt.Screen.Send(pass1+"\r")
			crt.Screen.WaitForString("EG>")

			if Port2 != "@" :
				crt.Screen.Send("show interfaces " + Port1 + " terse\r")
				#crt.Screen.WaitForString("--> ")
				WaPo = crt.Screen.WaitForStrings(['--> ','vpls','EG>'],5)
				if WaPo == 1:
					Port1 = crt.Screen.ReadString(".")
					GetINTPort = 0
				if WaPo == 2:
					GetINTPort = 1
				if WaPo == 3:
					crt.Screen.Send("\r")
					GetINTPort = 1
				crt.Screen.WaitForString("EG>")


			crt.Screen.Send('show configuration routing-instances ORANGE-VPLS-BITSTREAM | except "ORANGE-VPLS-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			IVPLSRows = []
			IVconfRow = crt.Screen.CurrentRow - 1
			readIVconfRow = crt.Screen.Get(IVconfRow, 1,IVconfRow,400).strip()
			IVPLSRows.append(readIVconfRow)

			while readIVconfRow.endswith("display set") == False:
				IVconfRow = IVconfRow - 1
				readIVconfRow = crt.Screen.Get(IVconfRow, 1,IVconfRow,400).strip()
				IVPLSRows.append(readIVconfRow)

			IVconfRow1 = "set routing-instances ORANGE-VPLS-BITSTREAM protocols vpls enable-mac-move-action"
			IVconfRow2 = "set routing-instances ORANGE-VPLS-BITSTREAM protocols vpls mac-table-size 2000"
			IVconfRow3 = "set routing-instances ORANGE-VPLS-BITSTREAM protocols vpls no-tunnel-services"
			IVconfRow4 = "set routing-instances ORANGE-VPLS-BITSTREAM protocols vpls vpls-id 3050"
			IVconfRow5 = "set routing-instances ORANGE-VPLS-BITSTREAM instance-type vpls"
			IVconfRow6 = "set routing-instances ORANGE-VPLS-BITSTREAM vlan-id all"
			IVconfRow7 = "set routing-instances ORANGE-VPLS-BITSTREAM protocols vpls interface"

			IVconfRow = [IVconfRow1 , IVconfRow2 , IVconfRow3 , IVconfRow4 , IVconfRow5 , IVconfRow6 , IVconfRow7]

			IVcRow = [0,0,0,0,0,0,0]
			for i in range (0, len(IVPLSRows)):
				if IVPLSRows[i] == IVconfRow[0]:
					IVcRow[0] = 1
				if IVPLSRows[i] == IVconfRow[1]:
					IVcRow[1] = 1
				if IVPLSRows[i] == IVconfRow[2]:
					IVcRow[2] = 1
				if IVPLSRows[i] == IVconfRow[3]:
					IVcRow[3] = 1
				if IVPLSRows[i] == IVconfRow[4]:
					IVcRow[4] = 1
				if IVPLSRows[i] == IVconfRow[5]:
					IVcRow[5] = 1
				if IVPLSRows[i].startswith(IVconfRow[6]) == True:
					IVcRow[6] = 1
					interPort0 = IVPLSRows[i].split("interface ")
					interPort1 = interPort0[1].split(".")
					interPort = interPort1[0]
					#crt.Dialog.MessageBox(str(interPort))
					if Port1 != interPort:
						Port1 = interPort
					GetINTPort = 0


			IVcRowPr1 = "-"
			for i in range (0, len(IVcRow)):
				if IVcRow[i] == 0:
					IVcRowPr1 = IVcRowPr1 + IVconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			IVcRowPr = "- NO Missing configuration" if IVcRowPr1 == "-" else IVcRowPr1


			if GetINTPort == 1:
				crt.Screen.Send("show vpls mac-table instance ORANGE-VPLS-BITSTREAM | no-more\r")
				crt.Screen.WaitForString("Routing instance : ORANGE-VPLS-BITSTREAM")
				readINTPortST = crt.Screen.ReadString("MAC flags")
				readINTPortrows = readINTPortST.splitlines()
				#readINTPortrows = [item.strip() for item in readINTPortrows]
				for i in range (0, len(readINTPortrows)):
					if ".3050" in readINTPortrows[i]:
						readINTPortrow1 = readINTPortrows[i]
						readINTPortrow2 = readINTPortrow1.split("D")
						readINTPortrow = readINTPortrow2[1].strip()
						Port12 = readINTPortrow.split(".")
						Port1 = Port12[0]
				crt.Screen.WaitForString("EG>")


			crt.Screen.Send("show configuration interfaces " + Port1 + ".3050 | display set\r")
			crt.Screen.WaitForString("EG>")

			IRows = []
			IconfRow = crt.Screen.CurrentRow - 1
			readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
			IRows.append(readIconfRow)

			while readIconfRow.endswith("display set") == False:
				IconfRow = IconfRow - 1
				readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
				IRows.append(readIconfRow)

			crt.Screen.Send("show configuration routing-instances ORANGE-VPLS-BITSTREAM interface " + Port1 + ".3050 | display set\r")
			crt.Screen.WaitForString("EG>")

			IconfRow2 = crt.Screen.CurrentRow - 1
			readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
			IRows.append(readIconfRow2)

			while readIconfRow2.endswith("display set") == False:
				IconfRow2 = IconfRow2 - 1
				readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
				IRows.append(readIconfRow2)

			IconfRow1 = "set interfaces " + Port1 + " unit 3050 encapsulation vlan-vpls"
			IconfRow2 = "set interfaces " + Port1 + " unit 3050 vlan-id-range 3050-3299"
			IconfRow3 = "set routing-instances ORANGE-VPLS-BITSTREAM interface " + Port1 + ".3050"
			IconfRow = [IconfRow1,IconfRow2,IconfRow3]
			IcRow = [0,0,0]
			for i in range (0, len(IRows)):
				if IRows[i] == IconfRow[0]:
					IcRow[0] = 1
				if IRows[i] == IconfRow[1]:
					IcRow[1] = 1
				if IRows[i] == IconfRow[2]:
					IcRow[2] = 1

			IcRowPr1 = "-"
			for i in range (0, len(IcRow)):
				if IcRow[i] == 0:
					IcRowPr1 = IcRowPr1 + IconfRow[i] + "\r"
			#crt.Dialog.MessageBox(cRowPr)
			IcRowPr = "- NO Missing configuration" if IcRowPr1 == "-" else IcRowPr1

			

			crt.Screen.Send("show vpls connections instance ORANGE-VPLS-BITSTREAM | no-more\r")
			crt.Screen.WaitForString("ORANGE-VPLS-BITSTREAM")
			OVBRead = crt.Screen.ReadString("EG>")


			INeigRows = OVBRead.splitlines()
			INeigRows = [item.strip() for item in INeigRows]

			"""
			INeigRow = crt.Screen.CurrentRow - 1
			readINeigRow = crt.Screen.Get(INeigRow, 1,INeigRow,400).strip()
			INeigRows.append(readINeigRow)

			while readINeigRow.endswith("ORANGE-VPLS-BITSTREAM") == False:
				INeigRow = INeigRow - 1
				readINeigRow = crt.Screen.Get(INeigRow, 1,INeigRow,400).strip()
				INeigRows.append(readINeigRow)
			"""
			for i in range (0, len(INeigRows)):
				if MXRouterIP + "(" in INeigRows[i]:
					Ivplsconnrow = INeigRows[i]
					#crt.Dialog.MessageBox(str(vplsconnrow))

			INTMACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 3050 and int(VlanNum) <= 3299:
						
					crt.Screen.Send("show vpls mac-table instance ORANGE-VPLS-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if "lsi" in VLANRows[j]:
							INTMACs.append("There is MAC from MX Router side [customer] for VLAN " + VlanNum)

						if Port1 +".3050" in VLANRows[j]:
							INTMACs.append("There is MAC from ORANGE side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					INTMACs.append(addVlan)

			IMACsPr1 = "-"
			INTMACs = list(dict.fromkeys(INTMACs))
			for i in range (0, len(INTMACs)):
				IMACsPr1 = IMACsPr1 + INTMACs[i] + "\r"

			IMACsPr = "- NO MACs received from both side" if IMACsPr1 == "-" else IMACsPr1

			crt.Screen.Send("show interfaces " + Port1 + " | no-more\r")
			crt.Screen.WaitForString("Physical link is")
			InterPortStatus = str(crt.Screen.ReadString("Interface index")).strip()

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match last \r")
			crt.Screen.WaitForString("(")
			InterPortLastFlap = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match rate \r")
			crt.Screen.WaitForString("Input rate")
			InterPortInputRate = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("Output rate")
			InterPortOutputRate = crt.Screen.ReadString(")")


			crt.Dialog.MessageBox("            *****ORANGE-VPLS-BITSTREAM*****\r\r* MX Router : " + AggRouter + "\r\r* MX Port : " + link + "\r\r* Status : UP\r\r* Checking MX Port configuration :\r" + cRowPr + "\r\r* Checking MX VPLS configuration :\r" + VcRowPr + "\r\r* vpls connections Status on MX :\r" + vplsconnrow + "\r\r* MACs on MX : \r" + MACsPr + "\r\r* Interconnection Router : "+ InterRouter + "\r\r* Interconnection Port : " + Port1 + "\r\r* Status : " + InterPortStatus + "\r\r* Last Flap : " + InterPortLastFlap + "\r\r* Input Rate" + InterPortInputRate + ")\r* Output Rate" + InterPortOutputRate + ")\r\r* Checking Interconnection Port configuration :\r" + IcRowPr + "\r\r* Checking Interconnection VPLS configuration :\r" + IVcRowPr + "\r\r* vpls connections Status on Interconnection :\r" + Ivplsconnrow + "\r\r* MACs on Interconnection : \r" + IMACsPr ,"Ahmed Elaraby", BUTTON_CANCEL + ICON_INFO)


#######################################################################################################    
########################################### ORANGE MOBILE #############################################
#######################################################################################################

def ORANGEMOB(user,pass1,link,AggRouter,InterRouter,Port1,Port2):
	crt.Screen.Send("show interfaces descriptions | match " + link + ".2000\r")
	crt.Screen.WaitForString("EG>")

	StatusRows = []
	PortRow = crt.Screen.CurrentRow - 1
	readPortRow1 = crt.Screen.Get(PortRow, 1,PortRow,200).strip()
	StatusRows.append(readPortRow1)

	while readPortRow1.endswith("2000") == False:
		PortRow = PortRow - 1
		readPortRow1 = crt.Screen.Get(PortRow, 1,PortRow,400).strip()
		StatusRows.append(readPortRow1)

	for i in range (0, len(StatusRows)):
		if StatusRows[i].startswith(link):
			readPortRow = StatusRows[i]


	if "up    down" in readPortRow :
		#crt.Dialog.MessageBox("up    down")
		crt.Screen.Send("clear vpls mac-move-action interface " + link + ".2000\r")
		crt.Dialog.MessageBox("check now as mac-move-action cleared")
		return 0
	if "down  up" in readPortRow :
		crt.Dialog.MessageBox("check port is disabled")
		return 0

	if "up    up" in readPortRow :
		#crt.Dialog.MessageBox("up    up")
		crt.Screen.Send("show configuration interfaces " + link + ".2000 | display set\r")
		crt.Screen.WaitForString("EG>")

		Rows = []
		confRow = crt.Screen.CurrentRow - 1
		readconfRow = crt.Screen.Get(confRow, 1,confRow,400).strip()
		Rows.append(readconfRow)

		while readconfRow.endswith("display set") == False:
			confRow = confRow - 1
			readconfRow = crt.Screen.Get(confRow, 1,confRow,400).strip()
			Rows.append(readconfRow)

		crt.Screen.Send("show configuration routing-instances ORANGE-MOB-BITSTREAM interface " + link + ".2000 | display set\r")
		crt.Screen.WaitForString("EG>")

		confRow2 = crt.Screen.CurrentRow - 1
		readconfRow2 = crt.Screen.Get(confRow2, 1,confRow2,400).strip()
		Rows.append(readconfRow2)

		while readconfRow2.endswith("display set") == False:
			confRow2 = confRow2 - 1
			readconfRow2 = crt.Screen.Get(confRow2, 1,confRow2,400).strip()
			Rows.append(readconfRow2)


		confRow1 = "set interfaces " + link + " unit 2000 encapsulation vlan-vpls"
		confRow2 = "set interfaces " + link + " unit 2000 vlan-id-range 2000-2049"
		confRow3 = "set routing-instances ORANGE-MOB-BITSTREAM interface " + link + ".2000"
		confRow = [confRow1,confRow2,confRow3]
		cRow = [0,0,0]
		for i in range (0, len(Rows)):
			if Rows[i] == confRow[0]:
				cRow[0] = 1
			if Rows[i] == confRow[1]:
				cRow[1] = 1
			if Rows[i] == confRow[2]:
				cRow[2] = 1

		cRowPr1 = "-"
		for i in range (0, len(cRow)):
			if cRow[i] == 0:
				cRowPr1 = cRowPr1 + confRow[i] + "\r"
		#crt.Dialog.MessageBox(cRowPr)
		cRowPr = "- NO Missing configuration" if cRowPr1 == "-" else cRowPr1


		if AggRouter == InterRouter :

			if Port2 != "@" :
				crt.Screen.Send("show interfaces " + Port1 + " terse\r")
				#crt.Screen.WaitForString("--> ")
				WaPo = crt.Screen.WaitForStrings(['--> ','vpls','EG>'],5)
				if WaPo == 1:
					Port1 = crt.Screen.ReadString(".")
					GetINTPort = 0
				if WaPo == 2:
					GetINTPort = 1
				if WaPo == 3:
					crt.Screen.Send("\r")
					GetINTPort = 1
				crt.Screen.WaitForString("EG>")

			crt.Screen.Send('show configuration routing-instances ORANGE-MOB-BITSTREAM | except "ORANGE-MOB-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			VPLSRows = []
			VconfRow = crt.Screen.CurrentRow - 1
			readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
			VPLSRows.append(readVconfRow)

			while readVconfRow.endswith("display set") == False:
				VconfRow = VconfRow - 1
				readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
				VPLSRows.append(readVconfRow)

			VconfRow1 = "set routing-instances ORANGE-MOB-BITSTREAM protocols vpls enable-mac-move-action"
			VconfRow2 = "set routing-instances ORANGE-MOB-BITSTREAM protocols vpls mac-table-size 2000"
			VconfRow3 = "set routing-instances ORANGE-MOB-BITSTREAM protocols vpls no-tunnel-services"
			VconfRow4 = "set routing-instances ORANGE-MOB-BITSTREAM protocols vpls vpls-id 2000"
			VconfRow5 = "set routing-instances ORANGE-MOB-BITSTREAM instance-type vpls"
			VconfRow6 = "set routing-instances ORANGE-MOB-BITSTREAM vlan-id all"
			VconfRow7 = "set routing-instances ORANGE-MOB-BITSTREAM protocols vpls interface"

			VconfRow = [VconfRow1 , VconfRow2 , VconfRow3 , VconfRow4 , VconfRow5 , VconfRow6 , VconfRow7]

			VcRow = [0,0,0,0,0,0,0]
			for i in range (0, len(VPLSRows)):
				if VPLSRows[i] == VconfRow[0]:
					VcRow[0] = 1
				if VPLSRows[i] == VconfRow[1]:
					VcRow[1] = 1
				if VPLSRows[i] == VconfRow[2]:
					VcRow[2] = 1
				if VPLSRows[i] == VconfRow[3]:
					VcRow[3] = 1
				if VPLSRows[i] == VconfRow[4]:
					VcRow[4] = 1
				if VPLSRows[i] == VconfRow[5]:
					VcRow[5] = 1
				if VPLSRows[i].startswith(VconfRow[6]) == True:
					VcRow[6] = 1
					interPort0 = VPLSRows[i].split("interface ")
					interPort1 = interPort0[1].split(".")
					interPort = interPort1[0]
					#crt.Dialog.MessageBox(str(interPort))
					if Port1 != interPort:
						Port1 = interPort
					GetINTPort = 0

			VcRowPr1 = "-"
			for i in range (0, len(VcRow)):
				if VcRow[i] == 0:
					VcRowPr1 = VcRowPr1 + VconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			VcRowPr = "- NO Missing configuration" if VcRowPr1 == "-" else VcRowPr1

			if GetINTPort == 1:
				crt.Screen.Send("show vpls mac-table instance ORANGE-MOB-BITSTREAM | no-more\r")
				crt.Screen.WaitForString("Routing instance : ORANGE-MOB-BITSTREAM")
				readINTPortST = crt.Screen.ReadString("MAC flags")
				readINTPortrows = readINTPortST.splitlines()
				#readINTPortrows = [item.strip() for item in readINTPortrows]
				for i in range (0, len(readINTPortrows)):
					if ".2000" in readINTPortrows[i]:
						readINTPortrow1 = readINTPortrows[i]
						readINTPortrow2 = readINTPortrow1.split("D")
						readINTPortrow = readINTPortrow2[1].strip()
						Port12 = readINTPortrow.split(".")
						Port1 = Port12[0]
				crt.Screen.WaitForString("EG>")


			crt.Screen.Send("show configuration interfaces " + Port1 + ".2000 | display set\r")
			crt.Screen.WaitForString("EG>")

			IRows = []
			IconfRow = crt.Screen.CurrentRow - 1
			readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
			IRows.append(readIconfRow)

			while readIconfRow.endswith("display set") == False:
				IconfRow = IconfRow - 1
				readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
				IRows.append(readIconfRow)

			crt.Screen.Send("show configuration routing-instances ORANGE-MOB-BITSTREAM interface " + Port1 + ".2000 | display set\r")
			crt.Screen.WaitForString("EG>")

			IconfRow2 = crt.Screen.CurrentRow - 1
			readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
			IRows.append(readIconfRow2)

			while readIconfRow2.endswith("display set") == False:
				IconfRow2 = IconfRow2 - 1
				readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
				IRows.append(readIconfRow2)

			IconfRow1 = "set interfaces " + Port1 + " unit 2000 encapsulation vlan-vpls"
			IconfRow2 = "set interfaces " + Port1 + " unit 2000 vlan-id-range 2000-2049"
			IconfRow3 = "set routing-instances ORANGE-MOB-BITSTREAM interface " + Port1 + ".2000"
			IconfRow = [IconfRow1,IconfRow2,IconfRow3]
			IcRow = [0,0,0]
			for i in range (0, len(IRows)):
				if IRows[i] == IconfRow[0]:
					IcRow[0] = 1
				if IRows[i] == IconfRow[1]:
					IcRow[1] = 1
				if IRows[i] == IconfRow[2]:
					IcRow[2] = 1

			IcRowPr1 = "-"
			for i in range (0, len(IcRow)):
				if IcRow[i] == 0:
					IcRowPr1 = IcRowPr1 + IconfRow[i] + "\r"
			#crt.Dialog.MessageBox(cRowPr)
			IcRowPr = "- NO Missing configuration" if IcRowPr1 == "-" else IcRowPr1


			vlanNums = crt.Dialog.Prompt("Please Enter affected VLANs seperating with space :","Ahmed Elaraby")
			VLANs = vlanNums.split()
			MACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 2000 and int(VlanNum) <= 2049:
						
					crt.Screen.Send("show vpls mac-table instance ORANGE-MOB-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if Port1 + ".2000" in VLANRows[j]:
							MACs.append("There is MAC from ETISALAT side for VLAN " + VlanNum)

						if link +".2000" in VLANRows[j]:
							MACs.append("There is MAC from Customer side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					MACs.append(addVlan)

			MACsPr1 = "-"
			MACs = list(dict.fromkeys(MACs))
			for i in range (0, len(MACs)):
				MACsPr1 = MACsPr1 + MACs[i] + "\r"

			MACsPr = "- NO MACs received from both side" if MACsPr1 == "-" else MACsPr1

			crt.Screen.Send("show interfaces " + Port1 + " | no-more\r")
			crt.Screen.WaitForString("Physical link is")
			InterPortStatus = str(crt.Screen.ReadString("Interface index")).strip()

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match last \r")
			crt.Screen.WaitForString("(")
			InterPortLastFlap = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match rate \r")
			crt.Screen.WaitForString("Input rate")
			InterPortInputRate = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("Output rate")
			InterPortOutputRate = crt.Screen.ReadString(")")




			crt.Dialog.MessageBox("            *****ORANGE-MOB-BITSTREAM*****\r\r* MX Router : " + AggRouter + "\r\r* MX Port : " + link + "\r\r* Status : UP\r\r* Checking MX Port configuration :\r" + cRowPr +  "\r\r* Checking VPLS configuration :\r" + VcRowPr + "\r\r* Interconnection Router : "+ InterRouter + "\r\r* Interconnection Port : " + Port1 + "\r\r* Status : " + InterPortStatus + "\r\r* Last Flap : " + InterPortLastFlap + "\r\r* Input Rate" + InterPortInputRate + ")\r* Output Rate" + InterPortOutputRate + ")\r\r* MACs : \r" + MACsPr ,"Ahmed Elaraby", BUTTON_CANCEL + ICON_INFO)



		if AggRouter != InterRouter :
			#crt.Dialog.MessageBox("AggRouter != InterRouter")
			crt.Screen.Send('show configuration routing-instances ORANGE-MOB-BITSTREAM | except "ORANGE-MOB-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			VPLSRows = []
			VconfRow = crt.Screen.CurrentRow - 1
			readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
			VPLSRows.append(readVconfRow)

			while readVconfRow.endswith("display set") == False:
				VconfRow = VconfRow - 1
				readVconfRow = crt.Screen.Get(VconfRow, 1,VconfRow,400).strip()
				VPLSRows.append(readVconfRow)

			VconfRow1 = "set routing-instances ORANGE-MOB-BITSTREAM protocols vpls enable-mac-move-action"
			VconfRow2 = "set routing-instances ORANGE-MOB-BITSTREAM protocols vpls mac-table-size 2000"
			VconfRow3 = "set routing-instances ORANGE-MOB-BITSTREAM protocols vpls no-tunnel-services"
			VconfRow4 = "set routing-instances ORANGE-MOB-BITSTREAM protocols vpls vpls-id 2000"
			VconfRow5 = "set routing-instances ORANGE-MOB-BITSTREAM instance-type vpls"
			VconfRow6 = "set routing-instances ORANGE-MOB-BITSTREAM vlan-id all"
			VconfRow7 = "set routing-instances ORANGE-MOB-BITSTREAM protocols vpls neighbor"

			VconfRow = [VconfRow1 , VconfRow2 , VconfRow3 , VconfRow4 , VconfRow5 , VconfRow6 , VconfRow7]

			VcRow = [0,0,0,0,0,0,0]
			neigIP = "@"
			for i in range (0, len(VPLSRows)):
				if VPLSRows[i] == VconfRow[0]:
					VcRow[0] = 1
				if VPLSRows[i] == VconfRow[1]:
					VcRow[1] = 1
				if VPLSRows[i] == VconfRow[2]:
					VcRow[2] = 1
				if VPLSRows[i] == VconfRow[3]:
					VcRow[3] = 1
				if VPLSRows[i] == VconfRow[4]:
					VcRow[4] = 1
				if VPLSRows[i] == VconfRow[5]:
					VcRow[5] = 1
				if VPLSRows[i].startswith(VconfRow[6]) == True:
					VcRow[6] = 1
					neigIP0 = VPLSRows[i].split("neighbor ")
					neigIP1 = neigIP0[1].split(" ")
					neigIP = neigIP1[0]

			"""
			if neigIP == "@":

				data =[]
				FileName = "Devices.csv"
				try:
					with open(os.path.join(os.path.dirname(__file__), FileName), mode='r') as csvfile:
						reader = csv.reader(csvfile)
						for row in reader:
							data.append(row)
				except EnvironmentError:
					crt.Dialog.MessageBox("Sorry Can't Open File! Please Change Files and Script Location!","Ahmed Elaraby")
					return 0

				TARGETCICol = [x[11] for x in data]
				if InterRouter in TARGETCICol:
					for x in range(0,len(data)):
						if InterRouter == data[x][11]:
							neigIP = data[x][5]

			"""

			VcRowPr1 = "-"
			for i in range (0, len(VcRow)):
				if VcRow[i] == 0:
					VcRowPr1 = VcRowPr1 + VconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			VcRowPr = "- NO Missing configuration" if VcRowPr1 == "-" else VcRowPr1

			crt.Screen.Send("show vpls connections instance ORANGE-MOB-BITSTREAM | no-more\r")
			crt.Screen.WaitForString("EG>")

			NeigRows = []
			NeigRow = crt.Screen.CurrentRow - 1
			readNeigRow = crt.Screen.Get(NeigRow, 1,NeigRow,400).strip()
			NeigRows.append(readNeigRow)

			while readNeigRow.endswith("ORANGE-MOB-BITSTREAM") == False:
				NeigRow = NeigRow - 1
				readNeigRow = crt.Screen.Get(NeigRow, 1,NeigRow,400).strip()
				NeigRows.append(readNeigRow)

			for i in range (0, len(NeigRows)):
				if NeigRows[i].startswith(neigIP):
					vplsconnrow = NeigRows[i]
					#crt.Dialog.MessageBox(str(vplsconnrow))


			vlanNums = crt.Dialog.Prompt("Please Enter affected VLANs seperating with space :","Ahmed Elaraby")
			VLANs = vlanNums.split()
			MXMACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 2000 and int(VlanNum) <= 2049:
						
					crt.Screen.Send("show vpls mac-table instance ORANGE-MOB-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if "lsi" in VLANRows[j]:
							MXMACs.append("There is MAC from Interconnection side [ORANGE] for VLAN " + VlanNum)

						if link +".2000" in VLANRows[j]:
							MXMACs.append("There is MAC from Customer side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					MXMACs.append(addVlan)

			MACsPr1 = "-"
			MXMACs = list(dict.fromkeys(MXMACs))
			for i in range (0, len(MXMACs)):
				MACsPr1 = MACsPr1 + MXMACs[i] + "\r"

			MACsPr = "- NO MACs received from both side" if MACsPr1 == "-" else MACsPr1

			crt.Screen.Send("show interfaces lo0.0\r")
			crt.Screen.WaitForString("Local: ")
			MXRouterIP = crt.Screen.ReadString("\r").strip()
			#crt.Dialog.MessageBox(MXRouterIP)

			crt.Screen.Send("quit\r")
			crt.Screen.WaitForString("~]$")

			if neigIP == "@":
				crt.Screen.Send("alias " + InterRouter + "\r")
				crt.Screen.WaitForString("telnet")
				neigIP = crt.Screen.ReadString("'").strip()
				crt.Screen.WaitForString("~]$")

			crt.Screen.Send("telnet " + neigIP + "\r")
			crt.Screen.WaitForString("login:")
			crt.Screen.Send(user+"\r")
			crt.Screen.WaitForString("Password:")
			crt.Screen.Send(pass1+"\r")
			crt.Screen.WaitForString("EG>")

			if Port2 != "@" :
				crt.Screen.Send("show interfaces " + Port1 + " terse\r")
				#crt.Screen.WaitForString("--> ")
				WaPo = crt.Screen.WaitForStrings(['--> ','vpls','EG>'],5)
				if WaPo == 1:
					Port1 = crt.Screen.ReadString(".")
					GetINTPort = 0
				if WaPo == 2:
					GetINTPort = 1
				if WaPo == 3:
					crt.Screen.Send("\r")
					GetINTPort = 1
				crt.Screen.WaitForString("EG>")


			crt.Screen.Send('show configuration routing-instances ORANGE-MOB-BITSTREAM | except "ORANGE-MOB-BITSTREAM interface" | display set\r')
			crt.Screen.WaitForString("EG>")

			IVPLSRows = []
			IVconfRow = crt.Screen.CurrentRow - 1
			readIVconfRow = crt.Screen.Get(IVconfRow, 1,IVconfRow,400).strip()
			IVPLSRows.append(readIVconfRow)

			while readIVconfRow.endswith("display set") == False:
				IVconfRow = IVconfRow - 1
				readIVconfRow = crt.Screen.Get(IVconfRow, 1,IVconfRow,400).strip()
				IVPLSRows.append(readIVconfRow)

			IVconfRow1 = "set routing-instances ORANGE-MOB-BITSTREAM protocols vpls enable-mac-move-action"
			IVconfRow2 = "set routing-instances ORANGE-MOB-BITSTREAM protocols vpls mac-table-size 2000"
			IVconfRow3 = "set routing-instances ORANGE-MOB-BITSTREAM protocols vpls no-tunnel-services"
			IVconfRow4 = "set routing-instances ORANGE-MOB-BITSTREAM protocols vpls vpls-id 2000"
			IVconfRow5 = "set routing-instances ORANGE-MOB-BITSTREAM instance-type vpls"
			IVconfRow6 = "set routing-instances ORANGE-MOB-BITSTREAM vlan-id all"
			IVconfRow7 = "set routing-instances ORANGE-MOB-BITSTREAM protocols vpls interface"

			IVconfRow = [IVconfRow1 , IVconfRow2 , IVconfRow3 , IVconfRow4 , IVconfRow5 , IVconfRow6 , IVconfRow7]

			IVcRow = [0,0,0,0,0,0,0]
			for i in range (0, len(IVPLSRows)):
				if IVPLSRows[i] == IVconfRow[0]:
					IVcRow[0] = 1
				if IVPLSRows[i] == IVconfRow[1]:
					IVcRow[1] = 1
				if IVPLSRows[i] == IVconfRow[2]:
					IVcRow[2] = 1
				if IVPLSRows[i] == IVconfRow[3]:
					IVcRow[3] = 1
				if IVPLSRows[i] == IVconfRow[4]:
					IVcRow[4] = 1
				if IVPLSRows[i] == IVconfRow[5]:
					IVcRow[5] = 1
				if IVPLSRows[i].startswith(IVconfRow[6]) == True:
					IVcRow[6] = 1
					interPort0 = IVPLSRows[i].split("interface ")
					interPort1 = interPort0[1].split(".")
					interPort = interPort1[0]
					#crt.Dialog.MessageBox(str(interPort))
					if Port1 != interPort:
						Port1 = interPort
					GetINTPort = 0


			IVcRowPr1 = "-"
			for i in range (0, len(IVcRow)):
				if IVcRow[i] == 0:
					IVcRowPr1 = IVcRowPr1 + IVconfRow[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			IVcRowPr = "- NO Missing configuration" if IVcRowPr1 == "-" else IVcRowPr1


			if GetINTPort == 1:
				crt.Screen.Send("show vpls mac-table instance ORANGE-MOB-BITSTREAM | no-more\r")
				crt.Screen.WaitForString("Routing instance : ORANGE-MOB-BITSTREAM")
				readINTPortST = crt.Screen.ReadString("MAC flags")
				readINTPortrows = readINTPortST.splitlines()
				#readINTPortrows = [item.strip() for item in readINTPortrows]
				for i in range (0, len(readINTPortrows)):
					if ".2000" in readINTPortrows[i]:
						readINTPortrow1 = readINTPortrows[i]
						readINTPortrow2 = readINTPortrow1.split("D")
						readINTPortrow = readINTPortrow2[1].strip()
						Port12 = readINTPortrow.split(".")
						Port1 = Port12[0]
				crt.Screen.WaitForString("EG>")


			crt.Screen.Send("show configuration interfaces " + Port1 + ".2000 | display set\r")
			crt.Screen.WaitForString("EG>")

			IRows = []
			IconfRow = crt.Screen.CurrentRow - 1
			readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
			IRows.append(readIconfRow)

			while readIconfRow.endswith("display set") == False:
				IconfRow = IconfRow - 1
				readIconfRow = crt.Screen.Get(IconfRow, 1,IconfRow,400).strip()
				IRows.append(readIconfRow)

			crt.Screen.Send("show configuration routing-instances ORANGE-MOB-BITSTREAM interface " + Port1 + ".2000 | display set\r")
			crt.Screen.WaitForString("EG>")

			IconfRow2 = crt.Screen.CurrentRow - 1
			readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
			IRows.append(readIconfRow2)

			while readIconfRow2.endswith("display set") == False:
				IconfRow2 = IconfRow2 - 1
				readIconfRow2 = crt.Screen.Get(IconfRow2, 1,IconfRow2,400).strip()
				IRows.append(readIconfRow2)

			IconfRow1 = "set interfaces " + Port1 + " unit 2000 encapsulation vlan-vpls"
			IconfRow2 = "set interfaces " + Port1 + " unit 2000 vlan-id-range 2000-2049"
			IconfRow3 = "set routing-instances ORANGE-MOB-BITSTREAM interface " + Port1 + ".2000"
			IconfRow = [IconfRow1,IconfRow2,IconfRow3]
			IcRow = [0,0,0]
			for i in range (0, len(IRows)):
				if IRows[i] == IconfRow[0]:
					IcRow[0] = 1
				if IRows[i] == IconfRow[1]:
					IcRow[1] = 1
				if IRows[i] == IconfRow[2]:
					IcRow[2] = 1

			IcRowPr1 = "-"
			for i in range (0, len(IcRow)):
				if IcRow[i] == 0:
					IcRowPr1 = IcRowPr1 + IconfRow[i] + "\r"
			#crt.Dialog.MessageBox(cRowPr)
			IcRowPr = "- NO Missing configuration" if IcRowPr1 == "-" else IcRowPr1

			

			crt.Screen.Send("show vpls connections instance ORANGE-MOB-BITSTREAM | no-more\r")
			crt.Screen.WaitForString("ORANGE-MOB-BITSTREAM")
			OVBRead = crt.Screen.ReadString("EG>")


			INeigRows = OVBRead.splitlines()
			INeigRows = [item.strip() for item in INeigRows]

			"""
			INeigRow = crt.Screen.CurrentRow - 1
			readINeigRow = crt.Screen.Get(INeigRow, 1,INeigRow,400).strip()
			INeigRows.append(readINeigRow)

			while readINeigRow.endswith("ORANGE-VPLS-BITSTREAM") == False:
				INeigRow = INeigRow - 1
				readINeigRow = crt.Screen.Get(INeigRow, 1,INeigRow,400).strip()
				INeigRows.append(readINeigRow)
			"""
			for i in range (0, len(INeigRows)):
				if MXRouterIP + "(" in INeigRows[i]:
					Ivplsconnrow = INeigRows[i]
					#crt.Dialog.MessageBox(str(vplsconnrow))

			INTMACs = []
			for i in range (0, len(VLANs)):
				#crt.Screen.WaitForString("EG>")
				VlanNum = VLANs[i]
				if int(VlanNum) >= 2000 and int(VlanNum) <= 2049:
						
					crt.Screen.Send("show vpls mac-table instance ORANGE-MOB-BITSTREAM vlan-id " + VlanNum + "\r")
					crt.Screen.WaitForString("-EG>")

					VLANRows = []
					VLANRow = crt.Screen.CurrentRow - 1
					readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
					VLANRows.append(readVLANRow)
							
					while readVLANRow.startswith(user) == False:
						VLANRow = VLANRow - 1
						readVLANRow = crt.Screen.Get(VLANRow, 1,VLANRow,300).strip()
						VLANRows.append(readVLANRow)
					#crt.Dialog.MessageBox(str(VLANRows))

					for j in range (0, len(VLANRows)):
								
						if "lsi" in VLANRows[j]:
							INTMACs.append("There is MAC from MX Router side [customer] for VLAN " + VlanNum)

						if Port1 +".2000" in VLANRows[j]:
							INTMACs.append("There is MAC from ORANGE side for VLAN " + VlanNum)


				else:
					addVlan = "VLAN " + VlanNum +" not in range"
					INTMACs.append(addVlan)

			IMACsPr1 = "-"
			INTMACs = list(dict.fromkeys(INTMACs))
			for i in range (0, len(INTMACs)):
				IMACsPr1 = IMACsPr1 + INTMACs[i] + "\r"

			IMACsPr = "- NO MACs received from both side" if IMACsPr1 == "-" else IMACsPr1

			crt.Screen.Send("show interfaces " + Port1 + " | no-more\r")
			crt.Screen.WaitForString("Physical link is")
			InterPortStatus = str(crt.Screen.ReadString("Interface index")).strip()

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match last \r")
			crt.Screen.WaitForString("(")
			InterPortLastFlap = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + Port1 + " | match rate \r")
			crt.Screen.WaitForString("Input rate")
			InterPortInputRate = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("Output rate")
			InterPortOutputRate = crt.Screen.ReadString(")")


			crt.Dialog.MessageBox("            *****ORANGE-MOB-BITSTREAM*****\r\r* MX Router : " + AggRouter + "\r\r* MX Port : " + link + "\r\r* Status : UP\r\r* Checking MX Port configuration :\r" + cRowPr + "\r\r* Checking MX VPLS configuration :\r" + VcRowPr + "\r\r* vpls connections Status on MX :\r" + vplsconnrow + "\r\r* MACs on MX : \r" + MACsPr + "\r\r* Interconnection Router : "+ InterRouter + "\r\r* Interconnection Port : " + Port1 + "\r\r* Status : " + InterPortStatus + "\r\r* Last Flap : " + InterPortLastFlap + "\r\r* Input Rate" + InterPortInputRate + ")\r* Output Rate" + InterPortOutputRate + ")\r\r* Checking Interconnection Port configuration :\r" + IcRowPr + "\r\r* Checking Interconnection VPLS configuration :\r" + IVcRowPr + "\r\r* vpls connections Status on Interconnection :\r" + Ivplsconnrow + "\r\r* MACs on Interconnection : \r" + IMACsPr ,"Ahmed Elaraby", BUTTON_CANCEL + ICON_INFO)


#######################################################################################################    
########################################### BITSTREAM #################################################
#######################################################################################################

def BITSTREAM(user,pass1,BTSVlan,link,MXRouter,linkStatus,BITSCOMType,BITSType):
	crt.Screen.Send("show interfaces descriptions | match " + link + "." + BTSVlan + "\r")
	crt.Screen.WaitForString("EG>")

	StatusRows = []
	readPortRow = "@"
	PortRow = crt.Screen.CurrentRow - 1
	readPortRow1 = crt.Screen.Get(PortRow, 1,PortRow,200).strip()
	StatusRows.append(readPortRow1)

	while readPortRow1.endswith(BTSVlan) == False:
		PortRow = PortRow - 1
		readPortRow1 = crt.Screen.Get(PortRow, 1,PortRow,400).strip()
		StatusRows.append(readPortRow1)

	for i in range (0, len(StatusRows)):
		if StatusRows[i].startswith(link):
			readPortRow = StatusRows[i]

	if readPortRow == "@":
		crt.Dialog.MessageBox("No Sub Interface Found!")
		return 0

	if "up    down" in readPortRow :

		crt.Dialog.MessageBox("Port connected to cabinet is Physical Down")
		return 0

	if "down  up" in readPortRow :

		crt.Dialog.MessageBox("check port is disabled")
		return 0

	if "down  down" in readPortRow :

		crt.Dialog.MessageBox("check port if disabled or physical Down")
		return 0

	if "up    up" in readPortRow :

		crt.Screen.Send("show configuration protocols l2circuit | match " + link + "." + BTSVlan + " | display set\r")
		crt.Screen.WaitForString("EG>")

		L2cirRows = []
		L2confRow = crt.Screen.CurrentRow - 1
		readL2confRow = crt.Screen.Get(L2confRow, 1,L2confRow,400).strip()
		L2cirRows.append(readL2confRow)

		while readL2confRow.endswith("display set") == False:
			L2confRow = L2confRow - 1
			readL2confRow = crt.Screen.Get(L2confRow, 1,L2confRow,400).strip()
			L2cirRows.append(readL2confRow)

		L2circonfRow1 = "interface " + link + "." + BTSVlan + " virtual-circuit-id"
		L2circonfRow2 = "interface " + link + "." + BTSVlan + " flow-label-transmit"
		L2circonfRow3 = "interface " + link + "." + BTSVlan + " flow-label-receive"
		L2circonfRow4 = "interface " + link + "." + BTSVlan + " mtu 1600"
					

		L2circonfRows = [L2circonfRow1 , L2circonfRow2 , L2circonfRow3 , L2circonfRow4]

		L2cRows = [0,0,0,0]
		NeigIP = "@"
		for i in range (0, len(L2cirRows)):
			if L2circonfRows[0] in L2cirRows[i]:
				L2cRows[0] = 1
				NeigIP0 = L2cirRows[i].split("neighbor ")
				NeigIP1 = NeigIP0[1].split(" interface")
				NeigIP = NeigIP1[0]

			if L2circonfRows[1] in L2cirRows[i]:
				L2cRows[1] = 1
			if L2circonfRows[2] in L2cirRows[i]:
				L2cRows[2] = 1
			if  L2circonfRows[3] in L2cirRows[i]:
				L2cRows[3] = 1
				NeigIP0 = L2cirRows[i].split("neighbor ")
				NeigIP1 = NeigIP0[1].split(" interface")
				NeigIP = NeigIP1[0]

		L2cRowPr1 = "-"
		for i in range (0, len(L2cRows)):
			if L2cRows[i] == 0:
				L2cRowPr1 = L2cRowPr1 + L2circonfRows[i] + "\r"
		#crt.Dialog.MessageBox(VcRowPr)
		L2cRowPr = "- NO Missing configuration" if L2cRowPr1 == "-" else L2cRowPr1

		crt.Screen.Send("show configuration interfaces " + link + "." + BTSVlan + " | display set\r")
		crt.Screen.WaitForString("EG>")

		IntRows = []
		IntconfRow = crt.Screen.CurrentRow - 1
		readIntconfRow = crt.Screen.Get(IntconfRow, 1,IntconfRow,400).strip()
		IntRows.append(readIntconfRow)

		while readIntconfRow.endswith("display set") == False:
			IntconfRow = IntconfRow - 1
			readIntconfRow = crt.Screen.Get(IntconfRow, 1,IntconfRow,400).strip()
			IntRows.append(readIntconfRow)

		IntconfRow1 = "set interfaces " + link + " unit " + BTSVlan + " encapsulation vlan-ccc"
		IntconfRow2 = "set interfaces " + link + " unit " + BTSVlan + " vlan-id " + BTSVlan
					
		IntconfRows = [IntconfRow1 , IntconfRow2]

		IntPRows = [0,0]
		for i in range (0, len(IntRows)):
			if IntRows[i] == IntconfRows[0]:
				IntPRows[0] = 1

			if IntRows[i] == IntconfRows[1]:
				IntPRows[1] = 1

		IntRowPr1 = "-"
		for i in range (0, len(IntPRows)):
			if IntPRows[i] == 0:
				IntRowPr1 = IntRowPr1 + IntconfRows[i] + "\r"
		#crt.Dialog.MessageBox(VcRowPr)
		IntRowPr = "- NO Missing configuration" if IntRowPr1 == "-" else IntRowPr1


		crt.Screen.Send("show l2circuit connections interface " + link + "." + BTSVlan + "\r")
		crt.Screen.WaitForString("EG>")

		L2StatusRows = []
		L2StatusRow = crt.Screen.CurrentRow - 1
		readL2StatusRow = crt.Screen.Get(L2StatusRow, 1,L2StatusRow,300).strip()
		L2StatusRows.append(readL2StatusRow)

		while readL2StatusRow.endswith("." + BTSVlan) == False:
			L2StatusRow = L2StatusRow - 1
			readL2StatusRow = crt.Screen.Get(L2StatusRow, 1,L2StatusRow,300).strip()
			L2StatusRows.append(readL2StatusRow)

		L2Status = "No Status Detected"
		VC = "@"
		for i in range (0, len(L2StatusRows)):
			if L2StatusRows[i].startswith(link) == True:
				L2Status = L2StatusRows[i]
				VC0 = L2Status.split("(vc")
				VC1 = VC0[1].split(")")
				VC = VC1[0].strip()

			if L2StatusRows[i].startswith("Neighbor") == True:
				nneigh0 = L2StatusRows[i].split(":")
				NeigIP = nneigh0[1].strip()

		if NeigIP == "@":
			crt.Dialog.MessageBox("No Neighbor Detected!")
			return 0

		if VC == "@":
			crt.Dialog.MessageBox("Check as No VC Found!")
			return 0

		crt.Screen.Send("show interfaces lo0.0\r")
		crt.Screen.WaitForString("Local: ")
		MXRouterIP = crt.Screen.ReadString("\r").strip()
		#crt.Dialog.MessageBox(MXRouterIP)

		crt.Screen.Send("quit\r")
		crt.Screen.WaitForString("~]$")

		crt.Screen.Send("telnet " + NeigIP + "\r")
		WSLogin = crt.Screen.WaitForStrings(['login:','Username:','@@@@@'],5)
		if WSLogin == 1:
			crt.Screen.Send(user + "\r")
			crt.Screen.WaitForString("Password:")
			crt.Screen.Send(pass1 + "\r")
			crt.Screen.WaitForString("EG>")

			crt.Screen.Send("\r")
			crt.Screen.WaitForString("@")
			AggrRouter = crt.Screen.ReadString(">")

			crt.Screen.Send("show l2circuit connections neighbor " + MXRouterIP + " | match " + VC + "\r")
			crt.Screen.WaitForString("EG>")

			AggL2StatusRows = []
			AggL2StatusRow = crt.Screen.CurrentRow - 1
			readAggL2StatusRow = crt.Screen.Get(AggL2StatusRow, 1,AggL2StatusRow,300).strip()
			AggL2StatusRows.append(readAggL2StatusRow)

			while readAggL2StatusRow.endswith(VC) == False:
				AggL2StatusRow = AggL2StatusRow - 1
				readAggL2StatusRow = crt.Screen.Get(AggL2StatusRow, 1,AggL2StatusRow,300).strip()
				AggL2StatusRows.append(readAggL2StatusRow)

			AggL2Status = "No Status Detected"
			VCin = "vc " + VC
			AggLink = "@"
			AggVlan = "@"
			for i in range (0, len(AggL2StatusRows)):
				if VCin in AggL2StatusRows[i]:
					AggL2Status = AggL2StatusRows[i]
					LinkVC0 = AggL2Status.split(".")
					AggLink = LinkVC0[0].strip()

					LinkVC1 = LinkVC0[1].split("(")
					AggVlan = LinkVC1[0].strip()

			if AggLink == "@" or AggVlan == "@":
				crt.Dialog.MessageBox("Check as No AggLink or AggVlan!")
				return 0

			crt.Screen.Send("show configuration interfaces " + AggLink + "." + AggVlan + " | display set\r")
			crt.Screen.WaitForString("EG>")

			IntL2cirRows = []
			IntL2confRow = crt.Screen.CurrentRow - 1
			readIntL2confRow = crt.Screen.Get(IntL2confRow, 1,IntL2confRow,400).strip()
			IntL2cirRows.append(readIntL2confRow)

			while readIntL2confRow.endswith("display set") == False:
				IntL2confRow = IntL2confRow - 1
				readIntL2confRow = crt.Screen.Get(IntL2confRow, 1,IntL2confRow,400).strip()
				IntL2cirRows.append(readIntL2confRow)

			IntL2circonfRow1 = "set interfaces " + AggLink + " unit " + AggVlan + " encapsulation vlan-ccc"
			IntL2circonfRow2 = "set interfaces " + AggLink + " unit " + AggVlan + " vlan-id " + AggVlan
			IntL2circonfRow3 = "set interfaces " + AggLink + " unit " + AggVlan + " input-vlan-map swap"
			IntL2circonfRow4 = "set interfaces " + AggLink + " unit " + AggVlan + " input-vlan-map vlan-id " + BTSVlan
			IntL2circonfRow5 = "set interfaces " + AggLink + " unit " + AggVlan + " output-vlan-map swap"

			IntL2circonfRows = [IntL2circonfRow1 , IntL2circonfRow2 , IntL2circonfRow3 , IntL2circonfRow4 , IntL2circonfRow5]

			IntL2cRows = [0,0,0,0,0]
			for i in range (0, len(IntL2cirRows)):
				if IntL2cirRows[i] == IntL2circonfRows[0]:
					IntL2cRows[0] = 1
				if IntL2cirRows[i] == IntL2circonfRows[1]:
					IntL2cRows[1] = 1
				if IntL2cirRows[i] == IntL2circonfRows[2]:
					IntL2cRows[2] = 1
				if IntL2cirRows[i] == IntL2circonfRows[3]:
					IntL2cRows[3] = 1
				if IntL2cirRows[i] == IntL2circonfRows[4]:
					IntL2cRows[4] = 1
								

			IntL2cRowPr1 = "-"
			for i in range (0, len(IntL2cRows)):
				if IntL2cRows[i] == 0:
					IntL2cRowPr1 = IntL2cRowPr1 + IntL2circonfRows[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			IntL2cRowPr = "- NO Missing configuration" if IntL2cRowPr1 == "-" else IntL2cRowPr1


			crt.Screen.Send("show configuration protocols l2circuit | match " + AggLink + "." + AggVlan + " | display set\r")
			crt.Screen.WaitForString("EG>")

			AggL2cirRows = []
			AggL2confRow = crt.Screen.CurrentRow - 1
			readAggL2confRow = crt.Screen.Get(AggL2confRow, 1,AggL2confRow,400).strip()
			AggL2cirRows.append(readAggL2confRow)

			while readAggL2confRow.endswith("display set") == False:
				AggL2confRow = AggL2confRow - 1
				readAggL2confRow = crt.Screen.Get(AggL2confRow, 1,AggL2confRow,400).strip()
				AggL2cirRows.append(readAggL2confRow)

			AggL2circonfRow1 = "set protocols l2circuit neighbor " + MXRouterIP + " interface " + AggLink + "." + AggVlan + " virtual-circuit-id " + VC 
			AggL2circonfRow2 = "set protocols l2circuit neighbor " + MXRouterIP + " interface " + AggLink + "." + AggVlan + " flow-label-transmit"
			AggL2circonfRow3 = "set protocols l2circuit neighbor " + MXRouterIP + " interface " + AggLink + "." + AggVlan + " flow-label-receive"
			AggL2circonfRow4 = "set protocols l2circuit neighbor " + MXRouterIP + " interface " + AggLink + "." + AggVlan + " mtu 1600"

			AggL2circonfRows = [AggL2circonfRow1 , AggL2circonfRow2 , AggL2circonfRow3 , AggL2circonfRow4]

			AggL2cRows = [0,0,0,0]
			for i in range (0, len(AggL2cirRows)):
				if AggL2cirRows[i] == AggL2circonfRows[0]:
					AggL2cRows[0] = 1
				if AggL2cirRows[i] == AggL2circonfRows[1]:
					AggL2cRows[1] = 1
				if AggL2cirRows[i] == AggL2circonfRows[2]:
					AggL2cRows[2] = 1
				if AggL2cirRows[i] == AggL2circonfRows[3]:
					AggL2cRows[3] = 1
								

			AggL2cRowPr1 = "-"
			for i in range (0, len(AggL2cRows)):
				if AggL2cRows[i] == 0:
					AggL2cRowPr1 = AggL2cRowPr1 + AggL2circonfRows[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			AggL2cRowPr = "- NO Missing configuration" if AggL2cRowPr1 == "-" else AggL2cRowPr1

			crt.Screen.Send("show interfaces " + AggLink + " | match last \r")
			crt.Screen.WaitForString("(")
			AggPortLastFlap = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + AggLink + " | match rate \r")
			crt.Screen.WaitForString("Input rate")
			AggPortInputRate = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("Output rate")
			AggPortOutputRate = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("quit\r")

			crt.Dialog.MessageBox("                *****" + BITSCOMType + " " + BITSType +"*****\r\r\r* MX Router : " + MXRouter + "\r\r* MX Port : " + link + "\r\r* MX Vlan : " + BTSVlan + "\r\r* MX Port Status : " + linkStatus + "\r\r* Checking MX Port configuration :\r" + IntRowPr + "\r\r* Checking L2VPN configuration :\r" + L2cRowPr + "\r\r* L2VPN Status on MX :\r"  + L2Status +  "\r\r* Aggregator Router : " + AggrRouter + "\r\r* Aggregator IP : " + NeigIP  + "\r\r* Aggregator Port : " + AggLink + "\r\r* Aggregator Vlan : " + AggVlan + "\r\r* Checking Aggregator Port configuration :\r" + IntL2cRowPr + "\r\r* Checking Aggregator L2VPN configuration :\r" + AggL2cRowPr + "\r\r* L2VPN Status on MX :\r" + AggL2Status + "\r\r* Last Flap : " + AggPortLastFlap + "\r\r* Input Rate" + AggPortInputRate + ")\r* Output Rate" + AggPortOutputRate + ")" ,"Ahmed Elaraby", BUTTON_CANCEL + ICON_INFO)


		if WSLogin == 2:
			crt.Screen.Send(user + "\r")
			crt.Screen.WaitForString("Password:")
			crt.Screen.Send(pass1 + "\r")
			crt.Screen.WaitForString("EG#")

			crt.Screen.Send("\r")
			crt.Screen.WaitForString(":")
			AggrRouter = crt.Screen.ReadString("#")

			crt.Screen.Send("show l2vpn xconnect neighbor " + MXRouterIP + " pw-id " + VC + "\r")
			crt.Screen.WaitForString("EG#")

			AggL2StatusRows = []
			AggL2StatusRow = crt.Screen.CurrentRow - 1
			readAggL2StatusRow = crt.Screen.Get(AggL2StatusRow, 1,AggL2StatusRow,300).strip()
			AggL2StatusRows.append(readAggL2StatusRow)

			while readAggL2StatusRow.endswith("EGY") == False:
				AggL2StatusRow = AggL2StatusRow - 1
				readAggL2StatusRow = crt.Screen.Get(AggL2StatusRow, 1,AggL2StatusRow,300).strip()
				AggL2StatusRows.append(readAggL2StatusRow)

			AggL2Status = "No Status Detected"
			xconnectGroup = "@"
			CabinetP2P = "@"
			AggLink = "@"
			AggVlan = "@"
			for i in range (0, len(AggL2StatusRows)):
				if VC in AggL2StatusRows[i]:
					AggL2Status = AggL2StatusRows[i]
					AggLink0 = AggL2StatusRows[i].split(".")
					AggLink1 = AggLink0[0].split("   ")
					AggLink = AggLink1[1]

					AggVlan0 = AggLink0[1].split(" ")
					AggVlan = AggVlan0[0]

					xconnectGroup = AggL2StatusRows[3]
					CabinetP2P = AggL2StatusRows[2]

					
			if AggLink == "@" or AggVlan == "@":
				crt.Dialog.MessageBox("Check as No AggLink or AggVlan!")
				return 0


			crt.Screen.Send("show running-config formal interface " + AggLink + "." + AggVlan + "\r")
			crt.Screen.WaitForString("EG#")

			IntL2cirRows = []
			IntL2confRow = crt.Screen.CurrentRow - 1
			readIntL2confRow = crt.Screen.Get(IntL2confRow, 1,IntL2confRow,400).strip()
			IntL2cirRows.append(readIntL2confRow)

			while readIntL2confRow.endswith(AggLink + "." + AggVlan) == False:
				IntL2confRow = IntL2confRow - 1
				readIntL2confRow = crt.Screen.Get(IntL2confRow, 1,IntL2confRow,400).strip()
				IntL2cirRows.append(readIntL2confRow)

			if AggLink.startswith("BE"):
				CAggLink = "Bundle-Ether" + AggLink[2:]
			if AggLink.startswith("Hu"):
				CAggLink = "HundredGigE" + AggLink[2:]
			if AggLink.startswith("Te"):
				CAggLink = "TenGigE" + AggLink[2:]
			if AggLink.startswith("Gi"):
				CAggLink = "GigabitEthernet" + AggLink[2:]

			IntL2circonfRow1 = "interface " + CAggLink + "." + AggVlan + " l2transport"
			IntL2circonfRow2 = "interface " + CAggLink + "." + AggVlan + " l2transport encapsulation dot1q " + AggVlan
			IntL2circonfRow3 = "interface " + CAggLink + "." + AggVlan + " l2transport rewrite ingress tag translate 1-to-1 dot1q " + BTSVlan + " symmetric"
			IntL2circonfRow4 = "interface " + CAggLink + "." + AggVlan + " l2transport mtu 1614"

			IntL2circonfRows = [IntL2circonfRow1 , IntL2circonfRow2 , IntL2circonfRow3 , IntL2circonfRow4]

			IntL2cRows = [0,0,0,0]
			for i in range (0, len(IntL2cirRows)):
				if IntL2cirRows[i] == IntL2circonfRows[0]:
					IntL2cRows[0] = 1
				if IntL2cirRows[i] == IntL2circonfRows[1]:
					IntL2cRows[1] = 1
				if IntL2cirRows[i] == IntL2circonfRows[2]:
					IntL2cRows[2] = 1
				if IntL2cirRows[i] == IntL2circonfRows[3]:
					IntL2cRows[3] = 1
								
			IntL2cRowPr1 = "-"
			for i in range (0, len(IntL2cRows)):
				if IntL2cRows[i] == 0:
					IntL2cRowPr1 = IntL2cRowPr1 + IntL2circonfRows[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			IntL2cRowPr = "- NO Missing configuration" if IntL2cRowPr1 == "-" else IntL2cRowPr1


			crt.Screen.Send("show running-config formal l2vpn xconnect group " + xconnectGroup + " p2p " + CabinetP2P + "\r")
			#crt.Screen.WaitForString("EG#")
			WSCommand = crt.Screen.WaitForStrings(['EG#','marker','@@@@@'],5)
			if WSCommand == 1:
				crt.Screen.Send("\r")
				crt.Screen.WaitForString("EG#")
			if WSCommand == 2:
				crt.Screen.WaitForString("EG#")
				xconnectGroup = AggL2StatusRows[4]
				CabinetP2P = AggL2StatusRows[3]
				crt.Screen.Send("show running-config formal l2vpn xconnect group " + xconnectGroup + " p2p " + CabinetP2P + "\r")
				WSCommand = crt.Screen.WaitForStrings(['EG#','marker','@@@@@'],5)
				if WSCommand == 1:
					crt.Screen.Send("\r")
					crt.Screen.WaitForString("EG#")
				if WSCommand == 2:
					crt.Screen.WaitForString("EG#")
					xconnAp2p = AggL2StatusRows[3].split("  ")
					xconnectGroup = xconnAp2p[0]
					CabinetP2P = xconnAp2p[1]
					crt.Screen.Send("show running-config formal l2vpn xconnect group " + xconnectGroup + " p2p " + CabinetP2P + "\r")
					crt.Screen.WaitForString("EG#")

			AggL2cirRows = []
			AggL2confRow = crt.Screen.CurrentRow - 1
			readAggL2confRow = crt.Screen.Get(AggL2confRow, 1,AggL2confRow,400).strip()
			AggL2cirRows.append(readAggL2confRow)

			while readAggL2confRow.endswith("EGY") == False:
				AggL2confRow = AggL2confRow - 1
				readAggL2confRow = crt.Screen.Get(AggL2confRow, 1,AggL2confRow,400).strip()
				AggL2cirRows.append(readAggL2confRow)

			AggL2circonfRow1 = "l2vpn xconnect group " + xconnectGroup + " p2p " + CabinetP2P  
			AggL2circonfRow2 = "l2vpn xconnect group " + xconnectGroup + " p2p " + CabinetP2P + " interface " + CAggLink + "." + AggVlan 
			AggL2circonfRow3 = "l2vpn xconnect group " + xconnectGroup + " p2p " + CabinetP2P + " neighbor ipv4 " + MXRouterIP + " pw-id " + VC  
			AggL2circonfRow4 = "l2vpn xconnect group " + xconnectGroup + " p2p " + CabinetP2P + " neighbor ipv4 " + MXRouterIP + " pw-id " + VC + " pw-class"

			AggL2circonfRows = [AggL2circonfRow1 , AggL2circonfRow2 , AggL2circonfRow3 , AggL2circonfRow4]

			AggL2cRows = [0,0,0,0]
			for i in range (0, len(AggL2cirRows)):
				if AggL2cirRows[i] == AggL2circonfRows[0]:
					AggL2cRows[0] = 1
				if AggL2cirRows[i] == AggL2circonfRows[1]:
					AggL2cRows[1] = 1
				if AggL2cirRows[i] == AggL2circonfRows[2]:
					AggL2cRows[2] = 1
				if AggL2circonfRows[3] in AggL2cirRows[i]:
					AggL2cRows[3] = 1
								

			AggL2cRowPr1 = "-"
			for i in range (0, len(AggL2cRows)):
				if AggL2cRows[i] == 0:
					AggL2cRowPr1 = AggL2cRowPr1 + AggL2circonfRows[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			AggL2cRowPr = "- NO Missing configuration" if AggL2cRowPr1 == "-" else AggL2cRowPr1


			crt.Screen.Send("show interfaces " + AggLink + " | include Last\r")
			crt.Screen.WaitForString("link flapped")
			AggPortLastFlap = crt.Screen.ReadString("\r")

			crt.Screen.WaitForString("EG#")
			crt.Screen.Send("show interfaces " + AggLink + " | include rate\r")
			crt.Screen.WaitForString("input rate")
			AggPortInputRate = crt.Screen.ReadString("packets/sec")

			crt.Screen.WaitForString("output rate")
			AggPortOutputRate = crt.Screen.ReadString("packets/sec")

			crt.Screen.WaitForString("EG#")
			crt.Screen.Send("exit\r")

			crt.Dialog.MessageBox("          *****" + BITSCOMType + " " + BITSType +"*****\r\r\r* MX Router : " + MXRouter + "\r\r* MX Port : " + link + "\r\r* MX Vlan : " + BTSVlan + "\r\r* MX Port Status : " + linkStatus + "\r\r* Checking MX Port configuration :\r" + IntRowPr + "\r\r* Checking L2VPN configuration :\r" + L2cRowPr + "\r\r* L2VPN Status on MX :\r"  + L2Status +  "\r\r* Aggregator Router : " + AggrRouter + "\r\r* Aggregator IP : " + NeigIP  + "\r\r* Aggregator Port : " + AggLink + "\r\r* Aggregator Vlan : " + AggVlan + "\r\r* Checking Aggregator Port configuration :\r" + IntL2cRowPr + "\r\r* Checking Aggregator L2VPN configuration :\r" + AggL2cRowPr + "\r\r* L2VPN Status on MX :\r" + AggL2Status + "\r\r* Last Flap : " + AggPortLastFlap + "\r\r* Input Rate : " + AggPortInputRate + "packets/sec\r* Output Rate : " + AggPortOutputRate + "packets/sec","Ahmed Elaraby", BUTTON_CANCEL + ICON_INFO )



#######################################################################################################    
########################################### L2VPN #####################################################
#######################################################################################################

def L2VPN(user,pass1):

		SourceHost = crt.Dialog.Prompt( "Please Enter Source Host Name","Ahmed Elaraby")
		crt.Screen.Send(SourceHost + "\r")
	
		cmx = crt.Screen.WaitForStrings(['login:','Username:','~]$'],5)
		if cmx == 1:
			crt.Screen.Send(user+"\r")
			crt.Screen.WaitForString("Password:")
			crt.Screen.Send(pass1+"\r")

			crt.Screen.WaitForString("EG>")
			SourcePort = crt.Dialog.Prompt( "Please Enter Source Port","Ahmed Elaraby")
			SourceVlan = crt.Dialog.Prompt( "Please Enter Source VLAN","Ahmed Elaraby")

			crt.Screen.Send("\r")
			crt.Screen.WaitForString("@")
			MXRouter = crt.Screen.ReadString(">")

			crt.Screen.Send("show interfaces " + SourcePort +" media\r")
			#crt.Screen.WaitForString("EG>")

			crt.Screen.WaitForString("Physical link is")
			PortStatus = str(crt.Screen.ReadString("Interface index")).strip()

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + SourcePort +" | match last\r")
			crt.Screen.WaitForString("(")
			LastFlap = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show interfaces " + SourcePort + " | match rate \r")

			crt.Screen.WaitForString("Input rate")
			InputRate = crt.Screen.ReadString(")")

			crt.Screen.WaitForString("Output rate")
			OutputRate = crt.Screen.ReadString(")")

			WSMore = crt.Screen.WaitForStrings(['(more)','EG>','~]$'],5)
			if WSMore == 1:
				crt.Screen.Send("\003")
			if WSMore == 2:
				crt.Screen.Send("\r")

			crt.Screen.WaitForString("EG>")
			crt.Screen.Send("show l2circuit connections interface " + SourcePort + "." + SourceVlan + "\r")
			crt.Screen.WaitForString("EG>")
				
			L2StatusRows = []
			L2StatusRow = crt.Screen.CurrentRow - 1
			readL2StatusRow = crt.Screen.Get(L2StatusRow, 1,L2StatusRow,300).strip()
			L2StatusRows.append(readL2StatusRow)

			while readL2StatusRow.endswith("." + SourceVlan) == False:
				L2StatusRow = L2StatusRow - 1
				readL2StatusRow = crt.Screen.Get(L2StatusRow, 1,L2StatusRow,300).strip()
				L2StatusRows.append(readL2StatusRow)

			L2Status = "No Status Detected"
			VC = "@"
			for i in range (0, len(L2StatusRows)):
				if L2StatusRows[i].startswith(SourcePort) == True:
					L2Status = L2StatusRows[i]
					VC0 = L2Status.split("(vc")
					VC1 = VC0[1].split(")")
					VC = VC1[0].strip()

				if L2StatusRows[i].startswith("Neighbor") == True:
					nneigh0 = L2StatusRows[i].split(":")
					NeigIP = nneigh0[1].strip()

			if NeigIP == "@":
				crt.Dialog.MessageBox("No Neighbor Detected!")
				return 0

			if VC == "@":
				crt.Dialog.MessageBox("Check as No VC Found!")
				return 0

			crt.Screen.Send("show configuration protocols l2circuit | match " + SourcePort + "." + SourceVlan + " | display set\r")
			crt.Screen.WaitForString("EG>")

			L2cirRows = []
			L2confRow = crt.Screen.CurrentRow - 1
			readL2confRow = crt.Screen.Get(L2confRow, 1,L2confRow,400).strip()
			L2cirRows.append(readL2confRow)

			while readL2confRow.endswith("display set") == False:
				L2confRow = L2confRow - 1
				readL2confRow = crt.Screen.Get(L2confRow, 1,L2confRow,400).strip()
				L2cirRows.append(readL2confRow)

			L2circonfRow1 = "interface " + SourcePort + "." + SourceVlan + " virtual-circuit-id"
			L2circonfRow2 = "interface " + SourcePort + "." + SourceVlan + " flow-label-transmit"
			L2circonfRow3 = "interface " + SourcePort + "." + SourceVlan + " flow-label-receive"
			L2circonfRow4 = "interface " + SourcePort + "." + SourceVlan + " mtu 1600"
					

			L2circonfRows = [L2circonfRow1 , L2circonfRow2 , L2circonfRow3 , L2circonfRow4]

			L2cRows = [0,0,0,0]
			NeigIP = "@"
			for i in range (0, len(L2cirRows)):
				if L2circonfRows[0] in L2cirRows[i]:
					L2cRows[0] = 1
					NeigIP0 = L2cirRows[i].split("neighbor ")
					NeigIP1 = NeigIP0[1].split(" interface")
					NeigIP = NeigIP1[0]

				if L2circonfRows[1] in L2cirRows[i]:
					L2cRows[1] = 1
				if L2circonfRows[2] in L2cirRows[i]:
					L2cRows[2] = 1
				if  L2circonfRows[3] in L2cirRows[i]:
					L2cRows[3] = 1
					NeigIP0 = L2cirRows[i].split("neighbor ")
					NeigIP1 = NeigIP0[1].split(" interface")
					NeigIP = NeigIP1[0]

			L2cRowPr1 = "-"
			for i in range (0, len(L2cRows)):
				if L2cRows[i] == 0:
					L2cRowPr1 = L2cRowPr1 + L2circonfRows[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			L2cRowPr = "- NO Missing configuration" if L2cRowPr1 == "-" else L2cRowPr1

			crt.Screen.Send("show configuration interfaces " + SourcePort + "." + SourceVlan + " | display set\r")
			crt.Screen.WaitForString("EG>")

			IntRows = []
			IntconfRow = crt.Screen.CurrentRow - 1
			readIntconfRow = crt.Screen.Get(IntconfRow, 1,IntconfRow,400).strip()
			IntRows.append(readIntconfRow)

			while readIntconfRow.endswith("display set") == False:
				IntconfRow = IntconfRow - 1
				readIntconfRow = crt.Screen.Get(IntconfRow, 1,IntconfRow,400).strip()
				IntRows.append(readIntconfRow)

			IntconfRow1 = "set interfaces " + SourcePort + " unit " + SourceVlan + " encapsulation vlan-ccc"
			IntconfRow2 = "set interfaces " + SourcePort + " unit " + SourceVlan + " vlan-id " + SourceVlan
					
			IntconfRows = [IntconfRow1 , IntconfRow2]

			IntPRows = [0,0]
			for i in range (0, len(IntRows)):
				if IntRows[i] == IntconfRows[0]:
					IntPRows[0] = 1

				if IntRows[i] == IntconfRows[1]:
					IntPRows[1] = 1

			IntRowPr1 = "-"
			for i in range (0, len(IntPRows)):
				if IntPRows[i] == 0:
					IntRowPr1 = IntRowPr1 + IntconfRows[i] + "\r"
			#crt.Dialog.MessageBox(VcRowPr)
			IntRowPr = "- NO Missing configuration" if IntRowPr1 == "-" else IntRowPr1

			crt.Screen.Send("show interfaces lo0.0\r")
			crt.Screen.WaitForString("Local: ")
			MXRouterIP = crt.Screen.ReadString("\r").strip()
			#crt.Dialog.MessageBox(MXRouterIP)

			crt.Screen.Send("quit\r")
			crt.Screen.WaitForString("~]$")
			crt.Screen.Send("telnet " + NeigIP + "\r")

			WSLogin = crt.Screen.WaitForStrings(['login:','Username:','@@@@@'],5)
			if WSLogin == 1:
				crt.Screen.Send(user + "\r")
				crt.Screen.WaitForString("Password:")
				crt.Screen.Send(pass1 + "\r")
				crt.Screen.WaitForString("EG>")

				crt.Screen.Send("\r")
				crt.Screen.WaitForString("@")
				AggrRouter = crt.Screen.ReadString(">")

				crt.Screen.Send("show l2circuit connections neighbor " + MXRouterIP + " | match " + VC + "\r")
				crt.Screen.WaitForString("EG>")

				AggL2StatusRows = []
				AggL2StatusRow = crt.Screen.CurrentRow - 1
				readAggL2StatusRow = crt.Screen.Get(AggL2StatusRow, 1,AggL2StatusRow,300).strip()
				AggL2StatusRows.append(readAggL2StatusRow)

				while readAggL2StatusRow.endswith(VC) == False:
					AggL2StatusRow = AggL2StatusRow - 1
					readAggL2StatusRow = crt.Screen.Get(AggL2StatusRow, 1,AggL2StatusRow,300).strip()
					AggL2StatusRows.append(readAggL2StatusRow)

				AggL2Status = "No Status Detected"
				VCin = "vc " + VC
				AggLink = "@"
				AggVlan = "@"
				for i in range (0, len(AggL2StatusRows)):
					if VCin in AggL2StatusRows[i]:
						AggL2Status = AggL2StatusRows[i]
						LinkVC0 = AggL2Status.split(".")
						AggLink = LinkVC0[0].strip()

						LinkVC1 = LinkVC0[1].split("(")
						AggVlan = LinkVC1[0].strip()

				if AggLink == "@" or AggVlan == "@":
					crt.Dialog.MessageBox("Check as No AggLink or AggVlan!")
					return 0

				crt.Screen.Send("show configuration interfaces " + AggLink + "." + AggVlan + " | display set\r")
				crt.Screen.WaitForString("EG>")

				IntL2cirRows = []
				IntL2confRow = crt.Screen.CurrentRow - 1
				readIntL2confRow = crt.Screen.Get(IntL2confRow, 1,IntL2confRow,400).strip()
				IntL2cirRows.append(readIntL2confRow)

				while readIntL2confRow.endswith("display set") == False:
					IntL2confRow = IntL2confRow - 1
					readIntL2confRow = crt.Screen.Get(IntL2confRow, 1,IntL2confRow,400).strip()
					IntL2cirRows.append(readIntL2confRow)

				IntL2circonfRow1 = "set interfaces " + AggLink + " unit " + AggVlan + " encapsulation vlan-ccc"
				IntL2circonfRow2 = "set interfaces " + AggLink + " unit " + AggVlan + " vlan-id " + AggVlan

				IntL2circonfRows = [IntL2circonfRow1 , IntL2circonfRow2]

				IntL2cRows = [0,0]
				for i in range (0, len(IntL2cirRows)):
					if IntL2cirRows[i] == IntL2circonfRows[0]:
						IntL2cRows[0] = 1
					if IntL2cirRows[i] == IntL2circonfRows[1]:
						IntL2cRows[1] = 1
								

				IntL2cRowPr1 = "-"
				for i in range (0, len(IntL2cRows)):
					if IntL2cRows[i] == 0:
						IntL2cRowPr1 = IntL2cRowPr1 + IntL2circonfRows[i] + "\r"
				#crt.Dialog.MessageBox(VcRowPr)
				IntL2cRowPr = "- NO Missing configuration" if IntL2cRowPr1 == "-" else IntL2cRowPr1


				crt.Screen.Send("show configuration protocols l2circuit | match " + AggLink + "." + AggVlan + " | display set\r")
				crt.Screen.WaitForString("EG>")

				AggL2cirRows = []
				AggL2confRow = crt.Screen.CurrentRow - 1
				readAggL2confRow = crt.Screen.Get(AggL2confRow, 1,AggL2confRow,400).strip()
				AggL2cirRows.append(readAggL2confRow)

				while readAggL2confRow.endswith("display set") == False:
					AggL2confRow = AggL2confRow - 1
					readAggL2confRow = crt.Screen.Get(AggL2confRow, 1,AggL2confRow,400).strip()
					AggL2cirRows.append(readAggL2confRow)

				AggL2circonfRow1 = "set protocols l2circuit neighbor " + MXRouterIP + " interface " + AggLink + "." + AggVlan + " virtual-circuit-id " + VC 
				AggL2circonfRow2 = "set protocols l2circuit neighbor " + MXRouterIP + " interface " + AggLink + "." + AggVlan + " flow-label-transmit"
				AggL2circonfRow3 = "set protocols l2circuit neighbor " + MXRouterIP + " interface " + AggLink + "." + AggVlan + " flow-label-receive"
				AggL2circonfRow4 = "set protocols l2circuit neighbor " + MXRouterIP + " interface " + AggLink + "." + AggVlan + " mtu 1600"

				AggL2circonfRows = [AggL2circonfRow1 , AggL2circonfRow2 , AggL2circonfRow3 , AggL2circonfRow4]

				AggL2cRows = [0,0,0,0]
				for i in range (0, len(AggL2cirRows)):
					if AggL2cirRows[i] == AggL2circonfRows[0]:
						AggL2cRows[0] = 1
					if AggL2cirRows[i] == AggL2circonfRows[1]:
						AggL2cRows[1] = 1
					if AggL2cirRows[i] == AggL2circonfRows[2]:
						AggL2cRows[2] = 1
					if AggL2cirRows[i] == AggL2circonfRows[3]:
						AggL2cRows[3] = 1
								

				AggL2cRowPr1 = "-"
				for i in range (0, len(AggL2cRows)):
					if AggL2cRows[i] == 0:
						AggL2cRowPr1 = AggL2cRowPr1 + AggL2circonfRows[i] + "\r"
				#crt.Dialog.MessageBox(VcRowPr)
				AggL2cRowPr = "- NO Missing configuration" if AggL2cRowPr1 == "-" else AggL2cRowPr1

				crt.Screen.Send("show interfaces " + AggLink + " | match last \r")
				crt.Screen.WaitForString("(")
				AggPortLastFlap = crt.Screen.ReadString(")")

				crt.Screen.WaitForString("EG>")
				crt.Screen.Send("show interfaces " + AggLink + " | match rate | no-more\r")
				crt.Screen.WaitForString("Input rate")
				AggPortInputRate = crt.Screen.ReadString(")")

				crt.Screen.WaitForString("Output rate")
				AggPortOutputRate = crt.Screen.ReadString(")")

				crt.Screen.WaitForString("EG>")
				crt.Screen.Send("quit\r")

				crt.Dialog.MessageBox("                ***** L2VPN *****\r\r\r* MX Router : " + MXRouter + "\r\r* MX Port : " + SourcePort + "\r\r* MX Vlan : " + SourceVlan + "\r\r* MX Port Status : " + PortStatus + "\r\r* Last Flap : " + LastFlap + "\r\r* Input Rate : " + InputRate + ")\r* Output Rate :" + OutputRate + ")\r\r* Checking MX Port configuration :\r" + IntRowPr + "\r\r* Checking L2VPN configuration :\r" + L2cRowPr + "\r\r* L2VPN Status on MX :\r"  + L2Status +  "\r\r* Aggregator Router : " + AggrRouter + "\r\r* Aggregator IP : " + NeigIP  + "\r\r* Aggregator Port : " + AggLink + "\r\r* Aggregator Vlan : " + AggVlan + "\r\r* Checking Aggregator Port configuration :\r" + IntL2cRowPr + "\r\r* Checking Aggregator L2VPN configuration :\r" + AggL2cRowPr + "\r\r* L2VPN Status on MX :\r" + AggL2Status + "\r\r* Last Flap : " + AggPortLastFlap + "\r\r* Input Rate" + AggPortInputRate + ")\r* Output Rate" + AggPortOutputRate + ")" ,"Ahmed Elaraby", BUTTON_CANCEL + ICON_INFO)

			if WSLogin == 2:
				crt.Screen.Send(user + "\r")
				crt.Screen.WaitForString("Password:")
				crt.Screen.Send(pass1 + "\r")
				crt.Screen.WaitForString("EG#")

				crt.Screen.Send("\r")
				crt.Screen.WaitForString(":")
				AggrRouter = crt.Screen.ReadString("#")

				crt.Screen.Send("show l2vpn xconnect neighbor " + MXRouterIP + " pw-id " + VC + "\r")
				crt.Screen.WaitForString("EG#")

				AggL2StatusRows = []
				AggL2StatusRow = crt.Screen.CurrentRow - 1
				readAggL2StatusRow = crt.Screen.Get(AggL2StatusRow, 1,AggL2StatusRow,300).strip()
				AggL2StatusRows.append(readAggL2StatusRow)

				while readAggL2StatusRow.endswith("EGY") == False:
					AggL2StatusRow = AggL2StatusRow - 1
					readAggL2StatusRow = crt.Screen.Get(AggL2StatusRow, 1,AggL2StatusRow,300).strip()
					AggL2StatusRows.append(readAggL2StatusRow)

				AggL2Status = "No Status Detected"
				xconnectGroup = "@"
				CabinetP2P = "@"
				AggLink = "@"
				AggVlan = "@"
				for i in range (0, len(AggL2StatusRows)):
					if VC in AggL2StatusRows[i]:
						AggL2Status = AggL2StatusRows[i]
						AggLink0 = AggL2StatusRows[i].split("   ")

						xconnectGroup = AggLink0[0]
						CabinetP2P = AggLink0[1]

						AggLink1 = AggLink0[3].split(".")
						AggLink = AggLink1[0]
						AggVlan = AggLink1[1]

					
				if AggLink == "@" or AggVlan == "@":
					crt.Dialog.MessageBox("Check as No AggLink or AggVlan!")
					return 0


				crt.Screen.Send("show running-config formal interface " + AggLink + "." + AggVlan + "\r")
				crt.Screen.WaitForString("EG#")

				IntL2cirRows = []
				IntL2confRow = crt.Screen.CurrentRow - 1
				readIntL2confRow = crt.Screen.Get(IntL2confRow, 1,IntL2confRow,400).strip()
				IntL2cirRows.append(readIntL2confRow)

				while readIntL2confRow.endswith(AggLink + "." + AggVlan) == False:
					IntL2confRow = IntL2confRow - 1
					readIntL2confRow = crt.Screen.Get(IntL2confRow, 1,IntL2confRow,400).strip()
					IntL2cirRows.append(readIntL2confRow)

				if AggLink.startswith("BE"):
					CAggLink = "Bundle-Ether" + AggLink[2:]
				if AggLink.startswith("Hu"):
					CAggLink = "HundredGigE" + AggLink[2:]
				if AggLink.startswith("Te"):
					CAggLink = "TenGigE" + AggLink[2:]
				if AggLink.startswith("Gi"):
					CAggLink = "GigabitEthernet" + AggLink[2:]

				IntL2circonfRow1 = "interface " + CAggLink + "." + AggVlan + " l2transport"
				IntL2circonfRow2 = "interface " + CAggLink + "." + AggVlan + " l2transport encapsulation dot1q " + AggVlan
				IntL2circonfRow3 = "interface " + CAggLink + "." + AggVlan + " l2transport mtu 1614"

				IntL2circonfRows = [IntL2circonfRow1 , IntL2circonfRow2 , IntL2circonfRow3]

				IntL2cRows = [0,0,0]
				for i in range (0, len(IntL2cirRows)):
					if IntL2cirRows[i] == IntL2circonfRows[0]:
						IntL2cRows[0] = 1
					if IntL2cirRows[i] == IntL2circonfRows[1]:
						IntL2cRows[1] = 1
					if IntL2cirRows[i] == IntL2circonfRows[2]:
						IntL2cRows[2] = 1
								
				IntL2cRowPr1 = "-"
				for i in range (0, len(IntL2cRows)):
					if IntL2cRows[i] == 0:
						IntL2cRowPr1 = IntL2cRowPr1 + IntL2circonfRows[i] + "\r"
				#crt.Dialog.MessageBox(VcRowPr)
				IntL2cRowPr = "- NO Missing configuration" if IntL2cRowPr1 == "-" else IntL2cRowPr1


				crt.Screen.Send("show running-config formal l2vpn xconnect group " + xconnectGroup + " p2p " + CabinetP2P + "\r")
				crt.Screen.WaitForString("EG#")
				
				AggL2cirRows = []
				AggL2confRow = crt.Screen.CurrentRow - 1
				readAggL2confRow = crt.Screen.Get(AggL2confRow, 1,AggL2confRow,400).strip()
				AggL2cirRows.append(readAggL2confRow)

				while readAggL2confRow.endswith("EGY") == False:
					AggL2confRow = AggL2confRow - 1
					readAggL2confRow = crt.Screen.Get(AggL2confRow, 1,AggL2confRow,400).strip()
					AggL2cirRows.append(readAggL2confRow)

				AggL2circonfRow1 = "l2vpn xconnect group " + xconnectGroup + " p2p " + CabinetP2P  
				AggL2circonfRow2 = "l2vpn xconnect group " + xconnectGroup + " p2p " + CabinetP2P + " interface " + CAggLink + "." + AggVlan 
				AggL2circonfRow3 = "l2vpn xconnect group " + xconnectGroup + " p2p " + CabinetP2P + " neighbor ipv4 " + MXRouterIP + " pw-id " + VC  
				AggL2circonfRow4 = "l2vpn xconnect group " + xconnectGroup + " p2p " + CabinetP2P + " neighbor ipv4 " + MXRouterIP + " pw-id " + VC + " pw-class"

				AggL2circonfRows = [AggL2circonfRow1 , AggL2circonfRow2 , AggL2circonfRow3 , AggL2circonfRow4]

				AggL2cRows = [0,0,0,0]
				for i in range (0, len(AggL2cirRows)):
					if AggL2cirRows[i] == AggL2circonfRows[0]:
						AggL2cRows[0] = 1
					if AggL2cirRows[i] == AggL2circonfRows[1]:
						AggL2cRows[1] = 1
					if AggL2cirRows[i] == AggL2circonfRows[2]:
						AggL2cRows[2] = 1
					if AggL2circonfRows[3] in AggL2cirRows[i]:
						AggL2cRows[3] = 1
								

				AggL2cRowPr1 = "-"
				for i in range (0, len(AggL2cRows)):
					if AggL2cRows[i] == 0:
						AggL2cRowPr1 = AggL2cRowPr1 + AggL2circonfRows[i] + "\r"
				#crt.Dialog.MessageBox(VcRowPr)
				AggL2cRowPr = "- NO Missing configuration" if AggL2cRowPr1 == "-" else AggL2cRowPr1


				crt.Screen.Send("show interfaces " + AggLink + " | include Last\r")
				crt.Screen.WaitForString("link flapped")
				AggPortLastFlap = crt.Screen.ReadString("\r")

				crt.Screen.WaitForString("EG#")
				crt.Screen.Send("show interfaces " + AggLink + " | include rate\r")
				crt.Screen.WaitForString("input rate")
				AggPortInputRate = crt.Screen.ReadString("packets/sec")

				crt.Screen.WaitForString("output rate")
				AggPortOutputRate = crt.Screen.ReadString("packets/sec")

				crt.Screen.WaitForString("EG#")
				crt.Screen.Send("exit\r")

				crt.Dialog.MessageBox("          ***** L2VPN *****\r\r\r* MX Router : " + MXRouter + "\r\r* MX Port : " + SourcePort + "\r\r* MX Vlan : " + SourceVlan + "\r\r* MX Port Status : " + PortStatus + "\r\r* Last Flap : " + LastFlap + "\r\r* Input Rate : " + InputRate + ")\r* Output Rate :" + OutputRate + ")\r\r* Checking MX Port configuration :\r" + IntRowPr + "\r\r* Checking L2VPN configuration :\r" + L2cRowPr + "\r\r* L2VPN Status on MX :\r"  + L2Status +  "\r\r* Aggregator Router : " + AggrRouter + "\r\r* Aggregator IP : " + NeigIP  + "\r\r* Aggregator Port : " + AggLink + "\r\r* Aggregator Vlan : " + AggVlan + "\r\r* Checking Aggregator Port configuration :\r" + IntL2cRowPr + "\r\r* Checking Aggregator L2VPN configuration :\r" + AggL2cRowPr + "\r\r* L2VPN Status on MX :\r" + AggL2Status + "\r\r* Last Flap : " + AggPortLastFlap + "\r\r* Input Rate : " + AggPortInputRate + "packets/sec\r* Output Rate : " + AggPortOutputRate + "packets/sec","Ahmed Elaraby", BUTTON_CANCEL + ICON_INFO )


		if cmx == 2:
			crt.Screen.Send(user+"\r")
			crt.Screen.WaitForString("Password:")
			crt.Screen.Send(pass1+"\r")

			crt.Dialog.MessageBox("Error")

		if cmx == 3:
			crt.Dialog.MessageBox("Can't access Router!","Ahmed Elaraby")


#######################################################################################################    
########################################### ALLBITSTREAM ##############################################
#######################################################################################################

def BITSTREAMALL(user,pass1):

		ip = crt.Dialog.Prompt("Please Enter IP :","Ahmed Elaraby").strip()
		mxip = ip.split('.')
		lip = int(mxip[3]) - 1

		#crt.Screen.WaitForString("~]$")
		crt.Screen.Send("telnet " +str(mxip[0])+"."+str(mxip[1])+"."+str(mxip[2])+"."+str(lip)+"\r")

		cmx = crt.Screen.WaitForStrings(['login:','~]$','@@@'],5)
		if cmx != 1 and cmx != 2 and cmx != 3:
			crt.Screen.Send("\003")
			cmx = crt.Screen.WaitForStrings(['login:','~]$','@@@'],5)

		while cmx == 2:
			crt.Screen.Send("telnet " +str(mxip[0])+"."+str(mxip[1])+"."+str(mxip[2])+"."+str(lip)+"\r")
			cmx = crt.Screen.WaitForStrings(['login:','~]$','@@@'],5)
			lip = lip - 1

			if cmx != 1 and cmx != 2 and cmx != 3:
				crt.Screen.Send("\003")
				cmx = crt.Screen.WaitForStrings(['login:','~]$','@@@'],5)

		if cmx == 1:
			crt.Screen.Send(user+"\r")
			crt.Screen.WaitForString("Password:")
			crt.Screen.Send(pass1+"\r")


		crt.Screen.WaitForString("EG>")
		crt.Screen.Send("show route " + ip + " table MSAN-TED-MNG.inet\r")
		crt.Screen.WaitForString("via")
		link = crt.Screen.ReadString(".").strip()

		crt.Screen.WaitForString("EG>")
		crt.Screen.Send("\r")
		crt.Screen.WaitForString("@")
		MXRouter = crt.Screen.ReadString(">")

		crt.Screen.Send("show interfaces " + link + " | no-more\r")
		crt.Screen.WaitForString("Physical link is")
		linkStatus = crt.Screen.ReadString("\r").strip()

		if linkStatus == "Down":
			crt.Dialog.MessageBox("Port connected to cabinet is Physical Down")
			return 0

		crt.Screen.WaitForString("EG>")

		BTSCOMType = int(crt.Dialog.Prompt( "Please choose BTSTRM Company :   1- ETISALAT    2- VODAFONE    3- NOOR    4- ORANGE","Ahmed Elaraby"))
		BTStype = int(crt.Dialog.Prompt( "Please choose BTSTRM Type :   1- UNLIMITED    2- LIMITED    3- HIGH SPEED","Ahmed Elaraby"))

		if BTSCOMType == 1:

			if BTStype == 1:
				BTSVlan = "1709"
				BITSCOMType = "ETISALAT"
				BITSType = "UNLIMITED"
				Bitstream = BITSTREAM(user,pass1,BTSVlan,link,MXRouter,linkStatus,BITSCOMType,BITSType)

			if BTStype == 2:
				crt.Dialog.MessageBox("Not Exist Now in Telecom Egypt!")

			if BTStype == 3:
				BTSVlan = "1711"
				BITSCOMType = "ETISALAT"
				BITSType = "HIGH SPEED"
				Bitstream = BITSTREAM(user,pass1,BTSVlan,link,MXRouter,linkStatus,BITSCOMType,BITSType)

		if BTSCOMType == 2:

			if BTStype == 1:
				BTSVlan = "1701"
				BITSCOMType = "VODAFONE"
				BITSType = "UNLIMITED"
				Bitstream = BITSTREAM(user,pass1,BTSVlan,link,MXRouter,linkStatus,BITSCOMType,BITSType)

			if BTStype == 2:
				crt.Dialog.MessageBox("Not Exist Now in Telecom Egypt!")

			if BTStype == 3:
				BTSVlan = "1703"
				BITSCOMType = "VODAFONE"
				BITSType = "HIGH SPEED"
				Bitstream = BITSTREAM(user,pass1,BTSVlan,link,MXRouter,linkStatus,BITSCOMType,BITSType)

		if BTSCOMType == 3:

			if BTStype == 1:
				BTSVlan = "1713"
				BITSCOMType = "NOOR"
				BITSType = "UNLIMITED"
				Bitstream = BITSTREAM(user,pass1,BTSVlan,link,MXRouter,linkStatus,BITSCOMType,BITSType)

			if BTStype == 2:
				crt.Dialog.MessageBox("Not Exist Now in Telecom Egypt!")

			if BTStype == 3:
				BTSVlan = "1715"
				BITSCOMType = "NOOR"
				BITSType = "HIGH SPEED"
				Bitstream = BITSTREAM(user,pass1,BTSVlan,link,MXRouter,linkStatus,BITSCOMType,BITSType)

		if BTSCOMType == 4:

			if BTStype == 1:
				BTSVlan = "1705"
				BITSCOMType = "ORANGE"
				BITSType = "UNLIMITED"
				Bitstream = BITSTREAM(user,pass1,BTSVlan,link,MXRouter,linkStatus,BITSCOMType,BITSType)

			if BTStype == 2:
				crt.Dialog.MessageBox("Not Exist Now in Telecom Egypt!")

			if BTStype == 3:
				BTSVlan = "1707"
				BITSCOMType = "ORANGE"
				BITSType = "HIGH SPEED"
				Bitstream = BITSTREAM(user,pass1,BTSVlan,link,MXRouter,linkStatus,BITSCOMType,BITSType)


#######################################################################################################    
########################################### SHBITSTREAM ###############################################
#######################################################################################################

def SHBITSTREAM(user,pass1):

		ip = crt.Dialog.Prompt("Please Enter IP :","Ahmed Elaraby").strip()
		mxip = ip.split('.')
		lip = int(mxip[3]) - 1

		#crt.Screen.WaitForString("~]$")
		crt.Screen.Send("telnet " +str(mxip[0])+"."+str(mxip[1])+"."+str(mxip[2])+"."+str(lip)+"\r")

		cmx = crt.Screen.WaitForStrings(['login:','~]$','@@@'],5)
		if cmx != 1 and cmx != 2 and cmx != 3:
			crt.Screen.Send("\003")
			cmx = crt.Screen.WaitForStrings(['login:','~]$','@@@'],5)

		while cmx == 2:
			crt.Screen.Send("telnet " +str(mxip[0])+"."+str(mxip[1])+"."+str(mxip[2])+"."+str(lip)+"\r")
			cmx = crt.Screen.WaitForStrings(['login:','~]$','@@@'],5)
			lip = lip - 1

			if cmx != 1 and cmx != 2 and cmx != 3:
				crt.Screen.Send("\003")
				cmx = crt.Screen.WaitForStrings(['login:','~]$','@@@'],5)

		if cmx == 1:
			crt.Screen.Send(user+"\r")
			crt.Screen.WaitForString("Password:")
			crt.Screen.Send(pass1+"\r")

		crt.Screen.WaitForString("@")
		RHostName = crt.Screen.ReadString("-R")
		HostName = RHostName + "-R"

		crt.Screen.WaitForString("J-")
		RegionName = crt.Screen.ReadString("-") 

		crt.Screen.WaitForString("EG>")
		crt.Screen.Send("\r")
		crt.Screen.WaitForString("@")
		AggRouter = crt.Screen.ReadString(">")

		#crt.Dialog.MessageBox(HostName + "\r" + RegionName + "\r" + AggRouter,"Ahmed Elaraby")

		filename="legislators-367011.json"
		

		Shtype = int(crt.Dialog.Prompt( "Please choose SHDSL BTSTRM Company :   1- ETISALAT    2- VODAFONE    3- NOOR    4- ORANGE","Ahmed Elaraby"))

		if Shtype == 1:
			Shtype2 = int(crt.Dialog.Prompt( "Please choose SHDSL BTSTRM Type :   1- ETISALAT-VPLS-BITSTREAM    2- ETISALAT-MOB-BITSTREAM   ","Ahmed Elaraby"))
			if Shtype2 == 1:
				sa = gspread.service_account(os.path.join(os.path.dirname(__file__), filename))

				sh = sa.open("ESP bitstream")

				wks1 = sh.worksheet("etisalat")

				records1 = wks1.get_values()
				dataframe1 = pd.DataFrame(records1)

				FNcount = dataframe1[3].str.contains(HostName).sum()
				if FNcount > 0 :
					use = dataframe1[dataframe1[3].str.contains(HostName) & dataframe1[3].str.contains(RegionName)].values[0]
					InterRouter = use[3]
					PortNum = use[4]
					#crt.Dialog.MessageBox(str(InterRouter) + "   " + str(PortNum))

				else :
					crt.Dialog.MessageBox("NO Active Interconnection!","Ahmed Elaraby")
					NOACTIVEINT = int(crt.Dialog.Prompt("DO you have Interconnection :  1- YES   2- NO","Ahmed Elaraby"))
					if NOACTIVEINT == 1:
						InterRouter = crt.Dialog.Prompt("Please Enter Interconnection Name : ","Ahmed Elaraby")
						PortNum = crt.Dialog.Prompt("Please Enter Interconnection Port : ","Ahmed Elaraby")
					if NOACTIVEINT == 2:
						crt.Dialog.MessageBox("You can back again after get Interconnection","Ahmed Elaraby")
						return 0

			if Shtype2 == 2:
				sa = gspread.service_account(os.path.join(os.path.dirname(__file__), filename))

				sh = sa.open("ESP bitstream")

				wks1 = sh.worksheet("ETISALAT-Mobile")

				records1 = wks1.get_values()
				dataframe1 = pd.DataFrame(records1)

				FNcount = dataframe1[3].str.contains(HostName).sum()
				if FNcount > 0 :
					use = dataframe1[dataframe1[3].str.contains(HostName) & dataframe1[3].str.contains(RegionName)].values[0]
					InterRouter = use[3]
					PortNum = use[4]
					#crt.Dialog.MessageBox(str(InterRouter) + "   " + str(PortNum))

				else :
					crt.Dialog.MessageBox("NO Active Interconnection!","Ahmed Elaraby")
					NOACTIVEINT = int(crt.Dialog.Prompt("DO you have Interconnection :  1- YES   2- NO","Ahmed Elaraby"))
					if NOACTIVEINT == 1:
						InterRouter = crt.Dialog.Prompt("Please Enter Interconnection Name : ","Ahmed Elaraby")
						PortNum = crt.Dialog.Prompt("Please Enter Interconnection Port : ","Ahmed Elaraby")
					if NOACTIVEINT == 2:
						crt.Dialog.MessageBox("You can back again after get Interconnection","Ahmed Elaraby")
						return 0

		if Shtype == 2:
			Shtype2 = int(crt.Dialog.Prompt( "Please choose SHDSL BTSTRM Type :   1- VODAFONE-VPLS-BITSTREAM    2- VODAFONE-MOB-BITSTREAM   ","Ahmed Elaraby"))
			if Shtype2 == 1:
				sa = gspread.service_account(os.path.join(os.path.dirname(__file__), filename))

				sh = sa.open("ESP bitstream")

				wks2 = sh.worksheet("Vodafone")

				records2 = wks2.get_values()
				dataframe2 = pd.DataFrame(records2)

				FNcount = dataframe2[2].str.contains(HostName).sum()
				if FNcount > 0 :
					use = dataframe2[dataframe2[2].str.contains(HostName) & dataframe2[2].str.contains(RegionName)].values[0]
					InterRouter = use[2]
					PortNum = use[3]
					#crt.Dialog.MessageBox(str(InterRouter) + "   " + str(PortNum))

				else :
					crt.Dialog.MessageBox("NO Active Interconnection!","Ahmed Elaraby")
					NOACTIVEINT = int(crt.Dialog.Prompt("DO you have Interconnection :  1- YES   2- NO","Ahmed Elaraby"))
					if NOACTIVEINT == 1:
						InterRouter = crt.Dialog.Prompt("Please Enter Interconnection Name : ","Ahmed Elaraby")
						PortNum = crt.Dialog.Prompt("Please Enter Interconnection Port : ","Ahmed Elaraby")
					if NOACTIVEINT == 2:
						crt.Dialog.MessageBox("You can back again after get Interconnection","Ahmed Elaraby")
						return 0
			
			if Shtype2 == 2:
				sa = gspread.service_account(os.path.join(os.path.dirname(__file__), filename))

				sh = sa.open("ESP bitstream")

				wks2 = sh.worksheet("Vodafone Mobil")

				records2 = wks2.get_values()
				dataframe2 = pd.DataFrame(records2)

				FNcount = dataframe2[1].str.contains(HostName).sum()
				if FNcount > 0 :
					use = dataframe2[dataframe2[1].str.contains(HostName) & dataframe2[1].str.contains(RegionName)].values[0]
					InterRouter = use[1]
					PortNum = use[2]
					#crt.Dialog.MessageBox(str(InterRouter) + "   " + str(PortNum))

				else :
					crt.Dialog.MessageBox("NO Active Interconnection!","Ahmed Elaraby")
					NOACTIVEINT = int(crt.Dialog.Prompt("DO you have Interconnection :  1- YES   2- NO","Ahmed Elaraby"))
					if NOACTIVEINT == 1:
						InterRouter = crt.Dialog.Prompt("Please Enter Interconnection Name : ","Ahmed Elaraby")
						PortNum = crt.Dialog.Prompt("Please Enter Interconnection Port : ","Ahmed Elaraby")
					if NOACTIVEINT == 2:
						crt.Dialog.MessageBox("You can back again after get Interconnection","Ahmed Elaraby")
						return 0

		if Shtype == 3:
			sa = gspread.service_account(os.path.join(os.path.dirname(__file__), filename))

			sh = sa.open("ESP bitstream")

			wks3 = sh.worksheet("NOOR")

			records3 = wks3.get_values()
			dataframe3 = pd.DataFrame(records3)

			FNcount = dataframe3[3].str.contains(HostName).sum()
			if FNcount > 0 :
				use = dataframe3[dataframe3[3].str.contains(HostName) & dataframe3[3].str.contains(RegionName)].values[0]
				InterRouter = use[3]
				PortNum = use[4]
				#crt.Dialog.MessageBox(str(InterRouter) + "   " + str(PortNum))

			else :
				crt.Dialog.MessageBox("NO Active Interconnection!","Ahmed Elaraby")
				NOACTIVEINT = int(crt.Dialog.Prompt("DO you have Interconnection :  1- YES   2- NO","Ahmed Elaraby"))
				if NOACTIVEINT == 1:
					InterRouter = crt.Dialog.Prompt("Please Enter Interconnection Name : ","Ahmed Elaraby")
					PortNum = crt.Dialog.Prompt("Please Enter Interconnection Port : ","Ahmed Elaraby")
				if NOACTIVEINT == 2:
					crt.Dialog.MessageBox("You can back again after get Interconnection","Ahmed Elaraby")
					return 0


		if Shtype == 4:
			Shtype2 = int(crt.Dialog.Prompt( "Please choose SHDSL BTSTRM Type :   1- ORANGE-VPLS-BITSTREAM    2- ORANGE-MOB-BITSTREAM   ","Ahmed Elaraby"))
			if Shtype2 == 1:
				sa = gspread.service_account(os.path.join(os.path.dirname(__file__), filename))

				sh = sa.open("ESP bitstream")

				wks4 = sh.worksheet("orange")
				
				records4 = wks4.get_values()
				dataframe4 = pd.DataFrame(records4)
				#crt.Dialog.MessageBox(str(dataframe4))

				FNcount = dataframe4[8].str.contains(HostName).sum()
				if FNcount > 0 :
					use = dataframe4[dataframe4[8].str.contains(HostName) & dataframe4[8].str.contains(RegionName)].values[0]
					InterRouter = use[8]
					PortNum = use[9]
					#crt.Dialog.MessageBox(str(InterRouter) + "   " + str(PortNum))

				else :
					crt.Dialog.MessageBox("NO Active Interconnection!","Ahmed Elaraby")
					NOACTIVEINT = int(crt.Dialog.Prompt("DO you have Interconnection :  1- YES   2- NO","Ahmed Elaraby"))
					if NOACTIVEINT == 1:
						InterRouter = crt.Dialog.Prompt("Please Enter Interconnection Name : ","Ahmed Elaraby")
						PortNum = crt.Dialog.Prompt("Please Enter Interconnection Port : ","Ahmed Elaraby")
					if NOACTIVEINT == 2:
						crt.Dialog.MessageBox("You can back again after get Interconnection","Ahmed Elaraby")
						return 0

			if Shtype2 == 2:
				sa = gspread.service_account(os.path.join(os.path.dirname(__file__), filename))

				sh = sa.open("ESP bitstream")

				wks4 = sh.get_worksheet(9)
				#worksheet_list = sh.worksheets()
				#crt.Dialog.MessageBox(str(worksheet_list))
				#return 0
				
				records4 = wks4.get_values()
				dataframe4 = pd.DataFrame(records4)
				#crt.Dialog.MessageBox(str(dataframe4))

				FNcount = dataframe4[8].str.contains(HostName).sum()
				if FNcount > 0 :
					use = dataframe4[dataframe4[8].str.contains(HostName) & dataframe4[8].str.contains(RegionName)].values[0]
					InterRouter = use[8]
					PortNum = use[9]
					#crt.Dialog.MessageBox(str(InterRouter) + "   " + str(PortNum))

				else :
					crt.Dialog.MessageBox("NO Active Interconnection!","Ahmed Elaraby")
					NOACTIVEINT = int(crt.Dialog.Prompt("DO you have Interconnection :  1- YES   2- NO","Ahmed Elaraby"))
					if NOACTIVEINT == 1:
						InterRouter = crt.Dialog.Prompt("Please Enter Interconnection Name : ","Ahmed Elaraby")
						PortNum = crt.Dialog.Prompt("Please Enter Interconnection Port : ","Ahmed Elaraby")
					if NOACTIVEINT == 2:
						crt.Dialog.MessageBox("You can back again after get Interconnection","Ahmed Elaraby")
						return 0

		#crt.Dialog.MessageBox(str(InterRouter) + "   " + str(PortNum))
		
		if "&" not in PortNum  and "," not in PortNum :
			Port1 = PortNum
			Port2 = "@"

		if "&" in PortNum :
			if "ae" in PortNum :
				PortNums = PortNum.split('&')
				PortNums2 = PortNums[1].split(' ')
				Port1 = PortNums[0].strip()
				Port2 = PortNums2[0].strip()
				
			if "ae" not in PortNum :
				PortNums = PortNum.split('&')
				Port1 = PortNums[0].strip()
				Port2 = PortNums[1].strip()
		if "," in PortNum :
			if "ae" in PortNum :
				PortNums = PortNum.split(',')
				PortNums2 = PortNums[1].split(' ')
				Port1 = PortNums[0].strip()
				Port2 = PortNums2[0].strip()
			if "ae" not in PortNum :
				PortNums = PortNum.split(',')
				Port1 = PortNums[0].strip()
				Port2 = PortNums[1].strip()
		if "&" not in PortNum and "," not in PortNum :
			Port2 = "$"

		

		

		crt.Screen.Send("show route " + ip + " table MSAN-TED-MNG.inet\r")
		crt.Screen.WaitForString("via")
		link = crt.Screen.ReadString(".").strip()

		crt.Screen.WaitForString("EG>")
		
		if Shtype == 1 and Shtype2 == 1:
			
			Etisalat = ETISALAT(user,pass1,link,AggRouter,InterRouter,Port1,Port2)

		if Shtype == 1 and Shtype2 == 2:
			
			Etisalat = ETISALATMOB(user,pass1,link,AggRouter,InterRouter,Port1,Port2)
			
		if Shtype == 2 and Shtype2 == 1:
			
			Vodafone = VODAFONE(user,pass1,link,AggRouter,InterRouter,Port1,Port2)

		if Shtype == 2 and Shtype2 == 2:
			
			Vodafone = VODAFONEMOB(user,pass1,link,AggRouter,InterRouter,Port1,Port2)

		if Shtype == 3:
			
			Noor = NOOR(user,pass1,link,AggRouter,InterRouter,Port1,Port2)

		if Shtype == 4 and Shtype2 == 1:
			
			Orange = ORANGE(user,pass1,link,AggRouter,InterRouter,Port1,Port2)

		if Shtype == 4 and Shtype2 == 2:
			
			Orange = ORANGEMOB(user,pass1,link,AggRouter,InterRouter,Port1,Port2)


####################################################################################################
########################################### MAIN ###################################################
####################################################################################################
####################################################################################################

def Main():

	objTab = crt.GetScriptTab()
	objConfig = objTab.Session.Config;

	objTab.Screen.Synchronous = True
	objTab.Screen.IgnoreEscape = True

	strValue = crt.Session.Config.GetOption("Keymap v5")

	value1 = strValue[0]
	value2 = strValue[1]
	x1 = value1.split('"')
	x2 = value2.split('"')
	
	user = x1[1]
	pass1 = x2[1]

	L2vpnType = int(crt.Dialog.Prompt( "Please choose Type :   1- L2VPN    2- BTSTRM    3- SHDSL BTSTRM","Ahmed Elaraby"))

	if L2vpnType == 1:
		
		L2vpn = L2VPN(user,pass1)
	
	if L2vpnType == 2:
		
		BitstreamAll = BITSTREAMALL(user,pass1)
		
	if L2vpnType == 3:
		
		SHBitstream = SHBITSTREAM(user,pass1)


Main()
