# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 876,603 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.olv_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.olv_sizer = wx.BoxSizer( wx.VERTICAL )
		
		
		self.olv_panel.SetSizer( self.olv_sizer )
		self.olv_panel.Layout()
		self.olv_sizer.Fit( self.olv_panel )
		bSizer2.Add( self.olv_panel, 1, wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menu1 = wx.Menu()
		self.m_menu11 = wx.Menu()
		self.m_menuItem1 = wx.MenuItem( self.m_menu11, wx.ID_ANY, u"Import from a CSV", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu11.AppendItem( self.m_menuItem1 )
		
		self.m_menuItem3 = wx.MenuItem( self.m_menu11, wx.ID_ANY, u"Import IP list", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu11.AppendItem( self.m_menuItem3 )
		
		self.m_menuItem4 = wx.MenuItem( self.m_menu11, wx.ID_ANY, u"Import Plot", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu11.AppendItem( self.m_menuItem4 )
		
		self.m_menu1.AppendSubMenu( self.m_menu11, u"Import" )
		
		self.m_menu2 = wx.Menu()
		self.m_menuItem8 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"Export to a CSV File", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu2.AppendItem( self.m_menuItem8 )
		
		self.m_menu1.AppendSubMenu( self.m_menu2, u"Export" )
		
		self.m_menuItem9 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Quit", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.AppendItem( self.m_menuItem9 )
		
		self.m_menubar1.Append( self.m_menu1, u"File" ) 
		
		self.m_menu5 = wx.Menu()
		self.m_menu3 = wx.Menu()
		self.m_menuItem10 = wx.MenuItem( self.m_menu3, wx.ID_ANY, u"Select All", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu3.AppendItem( self.m_menuItem10 )
		
		self.m_menuItem11 = wx.MenuItem( self.m_menu3, wx.ID_ANY, u"Select None", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu3.AppendItem( self.m_menuItem11 )
		
		self.m_menu5.AppendSubMenu( self.m_menu3, u"Select" )
		
		self.m_menuItem12 = wx.MenuItem( self.m_menu5, wx.ID_ANY, u"Preferences", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu5.AppendItem( self.m_menuItem12 )
		
		self.m_menubar1.Append( self.m_menu5, u"Edit" ) 
		
		self.m_menu6 = wx.Menu()
		self.m_menuItem13 = wx.MenuItem( self.m_menu6, wx.ID_ANY, u"Update Device Information", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu6.AppendItem( self.m_menuItem13 )
		
		self.m_menuItem14 = wx.MenuItem( self.m_menu6, wx.ID_ANY, u"Configure Device", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu6.AppendItem( self.m_menuItem14 )
		
		self.m_menuItem15 = wx.MenuItem( self.m_menu6, wx.ID_ANY, u"Send Commands", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu6.AppendItem( self.m_menuItem15 )
		
		self.m_menuItem16 = wx.MenuItem( self.m_menu6, wx.ID_ANY, u"Reset Factory", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu6.AppendItem( self.m_menuItem16 )
		
		self.m_menuItem17 = wx.MenuItem( self.m_menu6, wx.ID_ANY, u"Reboot Device", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu6.AppendItem( self.m_menuItem17 )
		
		self.m_menubar1.Append( self.m_menu6, u"Actions" ) 
		
		self.m_menu7 = wx.Menu()
		self.m_menuItem18 = wx.MenuItem( self.m_menu7, wx.ID_ANY, u"Ping Devices", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu7.AppendItem( self.m_menuItem18 )
		
		self.m_menuItem19 = wx.MenuItem( self.m_menu7, wx.ID_ANY, u"MSE Baseline", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu7.AppendItem( self.m_menuItem19 )
		
		self.m_menuItem20 = wx.MenuItem( self.m_menu7, wx.ID_ANY, u"Plot MSE", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu7.AppendItem( self.m_menuItem20 )
		
		self.m_menuItem21 = wx.MenuItem( self.m_menu7, wx.ID_ANY, u"Add line item", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu7.AppendItem( self.m_menuItem21 )
		
		self.m_menuItem22 = wx.MenuItem( self.m_menu7, wx.ID_ANY, u"Generate IP List", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu7.AppendItem( self.m_menuItem22 )
		
		self.m_menuItem23 = wx.MenuItem( self.m_menu7, wx.ID_ANY, u"Generate DGX List", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu7.AppendItem( self.m_menuItem23 )
		
		self.m_menubar1.Append( self.m_menu7, u"Tools" ) 
		
		self.m_menu8 = wx.Menu()
		self.m_menuItem24 = wx.MenuItem( self.m_menu8, wx.ID_ANY, u"Turn on LED's", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu8.AppendItem( self.m_menuItem24 )
		
		self.m_menuItem25 = wx.MenuItem( self.m_menu8, wx.ID_ANY, u"Turn off LED's", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu8.AppendItem( self.m_menuItem25 )
		
		self.m_menubar1.Append( self.m_menu8, u"Identify" ) 
		
		self.m_menu9 = wx.Menu()
		self.dhcp_sniffing_chk = wx.MenuItem( self.m_menu9, wx.ID_ANY, u"Listen for DHCP requests", wx.EmptyString, wx.ITEM_CHECK )
		self.m_menu9.AppendItem( self.dhcp_sniffing_chk )
		self.dhcp_sniffing_chk.Check( True )
		
		self.amx_only_filter_chk = wx.MenuItem( self.m_menu9, wx.ID_ANY, u"Only add AMX devices", wx.EmptyString, wx.ITEM_CHECK )
		self.m_menu9.AppendItem( self.amx_only_filter_chk )
		
		self.m_menubar1.Append( self.m_menu9, u"Listen" ) 
		
		self.m_menu10 = wx.Menu()
		self.m_menuItem34 = wx.MenuItem( self.m_menu10, wx.ID_ANY, u"Delete Item", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu10.AppendItem( self.m_menuItem34 )
		
		self.m_menuItem35 = wx.MenuItem( self.m_menu10, wx.ID_ANY, u"Delete All Items", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu10.AppendItem( self.m_menuItem35 )
		
		self.m_menubar1.Append( self.m_menu10, u"Delete" ) 
		
		self.m_menu111 = wx.Menu()
		self.m_menuItem36 = wx.MenuItem( self.m_menu111, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu111.AppendItem( self.m_menuItem36 )
		
		self.m_menubar1.Append( self.m_menu111, u"Help" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		self.status_bar = self.CreateStatusBar( 2, wx.ST_SIZEGRIP, wx.ID_ANY )
		self.rc_menu = wx.Menu()
		self.m_menuItem2 = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"Update device information", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.m_menuItem2 )
		
		self.m_menuItem251 = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"Configure Device", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.m_menuItem251 )
		
		self.m_menuItem261 = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"Send Commands", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.m_menuItem261 )
		
		self.m_menuItem271 = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"Reset Factory", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.m_menuItem271 )
		
		self.m_menuItem28 = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"Delete", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.m_menuItem28 )
		
		self.m_menuItem29 = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"Telnet to Device", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.m_menuItem29 )
		
		self.m_menuItem30 = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"FactoryAV", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.m_menuItem30 )
		
		self.m_menuItem31 = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"Reboot Device", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.m_menuItem31 )
		
		self.m_menuItem32 = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"MSE Baseline", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.m_menuItem32 )
		
		self.m_menuItem33 = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"Open device in webbrowser", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.m_menuItem33 )
		
		self.Bind( wx.EVT_RIGHT_DOWN, self.MainFrameOnContextMenu ) 
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.on_close )
		self.Bind( wx.EVT_MENU, self.import_csv_file, id = self.m_menuItem1.GetId() )
		self.Bind( wx.EVT_MENU, self.import_ip_list, id = self.m_menuItem3.GetId() )
		self.Bind( wx.EVT_MENU, self.import_plot, id = self.m_menuItem4.GetId() )
		self.Bind( wx.EVT_MENU, self.export_to_csv, id = self.m_menuItem8.GetId() )
		self.Bind( wx.EVT_MENU, self.on_quit, id = self.m_menuItem9.GetId() )
		self.Bind( wx.EVT_MENU, self.on_select_all, id = self.m_menuItem10.GetId() )
		self.Bind( wx.EVT_MENU, self.on_select_none, id = self.m_menuItem11.GetId() )
		self.Bind( wx.EVT_MENU, self.configure_prefs, id = self.m_menuItem12.GetId() )
		self.Bind( wx.EVT_MENU, self.get_config_info, id = self.m_menuItem13.GetId() )
		self.Bind( wx.EVT_MENU, self.configure_device, id = self.m_menuItem14.GetId() )
		self.Bind( wx.EVT_MENU, self.send_commands, id = self.m_menuItem15.GetId() )
		self.Bind( wx.EVT_MENU, self.reset_factory, id = self.m_menuItem16.GetId() )
		self.Bind( wx.EVT_MENU, self.reboot, id = self.m_menuItem17.GetId() )
		self.Bind( wx.EVT_MENU, self.multi_ping, id = self.m_menuItem18.GetId() )
		self.Bind( wx.EVT_MENU, self.mse_baseline, id = self.m_menuItem19.GetId() )
		self.Bind( wx.EVT_MENU, self.plot_mse, id = self.m_menuItem20.GetId() )
		self.Bind( wx.EVT_MENU, self.add_line, id = self.m_menuItem21.GetId() )
		self.Bind( wx.EVT_MENU, self.generate_list, id = self.m_menuItem22.GetId() )
		self.Bind( wx.EVT_MENU, self.generate_dgx_list, id = self.m_menuItem23.GetId() )
		self.Bind( wx.EVT_MENU, self.turn_on_leds, id = self.m_menuItem24.GetId() )
		self.Bind( wx.EVT_MENU, self.turn_off_leds, id = self.m_menuItem25.GetId() )
		self.Bind( wx.EVT_MENU, self.on_dhcp_sniffing, id = self.dhcp_sniffing_chk.GetId() )
		self.Bind( wx.EVT_MENU, self.on_amx_only_filter, id = self.amx_only_filter_chk.GetId() )
		self.Bind( wx.EVT_MENU, self.on_delete_item, id = self.m_menuItem34.GetId() )
		self.Bind( wx.EVT_MENU, self.delete_all_items, id = self.m_menuItem35.GetId() )
		self.Bind( wx.EVT_MENU, self.on_about_box, id = self.m_menuItem36.GetId() )
		self.Bind( wx.EVT_MENU, self.get_config_info, id = self.m_menuItem2.GetId() )
		self.Bind( wx.EVT_MENU, self.configure_device, id = self.m_menuItem251.GetId() )
		self.Bind( wx.EVT_MENU, self.send_commands, id = self.m_menuItem261.GetId() )
		self.Bind( wx.EVT_MENU, self.reset_factory, id = self.m_menuItem271.GetId() )
		self.Bind( wx.EVT_MENU, self.delete_item, id = self.m_menuItem28.GetId() )
		self.Bind( wx.EVT_MENU, self.telnet_to, id = self.m_menuItem29.GetId() )
		self.Bind( wx.EVT_MENU, self.factory_av, id = self.m_menuItem30.GetId() )
		self.Bind( wx.EVT_MENU, self.reboot, id = self.m_menuItem31.GetId() )
		self.Bind( wx.EVT_MENU, self.mse_baseline, id = self.m_menuItem32.GetId() )
		self.Bind( wx.EVT_MENU, self.open_url, id = self.m_menuItem33.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_close( self, event ):
		event.Skip()
	
	def import_csv_file( self, event ):
		event.Skip()
	
	def import_ip_list( self, event ):
		event.Skip()
	
	def import_plot( self, event ):
		event.Skip()
	
	def export_to_csv( self, event ):
		event.Skip()
	
	def on_quit( self, event ):
		event.Skip()
	
	def on_select_all( self, event ):
		event.Skip()
	
	def on_select_none( self, event ):
		event.Skip()
	
	def configure_prefs( self, event ):
		event.Skip()
	
	def get_config_info( self, event ):
		event.Skip()
	
	def configure_device( self, event ):
		event.Skip()
	
	def send_commands( self, event ):
		event.Skip()
	
	def reset_factory( self, event ):
		event.Skip()
	
	def reboot( self, event ):
		event.Skip()
	
	def multi_ping( self, event ):
		event.Skip()
	
	def mse_baseline( self, event ):
		event.Skip()
	
	def plot_mse( self, event ):
		event.Skip()
	
	def add_line( self, event ):
		event.Skip()
	
	def generate_list( self, event ):
		event.Skip()
	
	def generate_dgx_list( self, event ):
		event.Skip()
	
	def turn_on_leds( self, event ):
		event.Skip()
	
	def turn_off_leds( self, event ):
		event.Skip()
	
	def on_dhcp_sniffing( self, event ):
		event.Skip()
	
	def on_amx_only_filter( self, event ):
		event.Skip()
	
	def on_delete_item( self, event ):
		event.Skip()
	
	def delete_all_items( self, event ):
		event.Skip()
	
	def on_about_box( self, event ):
		event.Skip()
	
	
	
	
	
	def delete_item( self, event ):
		event.Skip()
	
	def telnet_to( self, event ):
		event.Skip()
	
	def factory_av( self, event ):
		event.Skip()
	
	
	
	def open_url( self, event ):
		event.Skip()
	
	def MainFrameOnContextMenu( self, event ):
		self.PopupMenu( self.rc_menu, event.GetPosition() )
		

###########################################################################
## Class PingDetail
###########################################################################

class PingDetail ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Details view", pos = wx.DefaultPosition, size = wx.Size( 390,550 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer21 = wx.BoxSizer( wx.VERTICAL )
		
		self.olv_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer24 = wx.BoxSizer( wx.VERTICAL )
		
		self.olv_sizer = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer24.Add( self.olv_sizer, 1, wx.EXPAND, 5 )
		
		bSizer23 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer26 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.auto_update_chk = wx.CheckBox( self.olv_panel, wx.ID_ANY, u"Auto update", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer26.Add( self.auto_update_chk, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer23.Add( bSizer26, 1, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer27 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_button4 = wx.Button( self.olv_panel, wx.ID_ANY, u"Refresh", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.m_button4, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer23.Add( bSizer27, 1, 0, 5 )
		
		
		bSizer24.Add( bSizer23, 0, wx.EXPAND, 5 )
		
		
		self.olv_panel.SetSizer( bSizer24 )
		self.olv_panel.Layout()
		bSizer24.Fit( self.olv_panel )
		bSizer21.Add( self.olv_panel, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer21 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.auto_update_chk.Bind( wx.EVT_CHECKBOX, self.on_auto_update )
		self.m_button4.Bind( wx.EVT_BUTTON, self.on_refresh )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_auto_update( self, event ):
		event.Skip()
	
	def on_refresh( self, event ):
		event.Skip()
	

###########################################################################
## Class Preferences
###########################################################################

class Preferences ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Preferences", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Configuration Default Values" ), wx.VERTICAL )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer14 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Master Address", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer14.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer14, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer13 = wx.BoxSizer( wx.VERTICAL )
		
		self.master_address_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.master_address_txt, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer11.Add( bSizer13, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		sbSizer1.Add( bSizer11, 1, wx.EXPAND, 5 )
		
		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Device Number", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer16.Add( self.m_staticText3, 0, wx.ALL, 5 )
		
		
		bSizer15.Add( bSizer16, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		self.device_number_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.device_number_txt, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer15.Add( bSizer17, 1, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		sbSizer1.Add( bSizer15, 1, wx.EXPAND, 5 )
		
		
		bSizer10.Add( sbSizer1, 0, wx.EXPAND|wx.ALL, 5 )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Notifications" ), wx.VERTICAL )
		
		self.success_chk = wx.CheckBox( self, wx.ID_ANY, u"Display Successful Connections", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.success_chk.SetValue(True) 
		sbSizer2.Add( self.success_chk, 0, wx.ALL, 5 )
		
		self.sounds_chk = wx.CheckBox( self, wx.ID_ANY, u"Play Sounds", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer2.Add( self.sounds_chk, 0, wx.ALL, 5 )
		
		
		bSizer10.Add( sbSizer2, 0, wx.EXPAND|wx.ALL, 5 )
		
		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Columns To Display" ), wx.VERTICAL )
		
		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.time_chk = wx.CheckBox( self, wx.ID_ANY, u"Time", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.time_chk, 0, wx.ALL, 5 )
		
		self.model_chk = wx.CheckBox( self, wx.ID_ANY, u"Model", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.model_chk, 0, wx.ALL, 5 )
		
		self.mac_chk = wx.CheckBox( self, wx.ID_ANY, u"MAC", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.mac_chk, 0, wx.ALL, 5 )
		
		self.ip_chk = wx.CheckBox( self, wx.ID_ANY, u"IP", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.ip_chk, 0, wx.ALL, 5 )
		
		self.hostname_chk = wx.CheckBox( self, wx.ID_ANY, u"Hostname", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.hostname_chk, 0, wx.ALL, 5 )
		
		self.serial_chk = wx.CheckBox( self, wx.ID_ANY, u"Serial Number", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.serial_chk, 0, wx.ALL, 5 )
		
		self.firmware_chk = wx.CheckBox( self, wx.ID_ANY, u"Firmware", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.firmware_chk, 0, wx.ALL, 5 )
		
		self.device_chk = wx.CheckBox( self, wx.ID_ANY, u"Device", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.device_chk, 0, wx.ALL, 5 )
		
		self.static_chk = wx.CheckBox( self, wx.ID_ANY, u"Static", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.static_chk, 0, wx.ALL, 5 )
		
		self.master_chk = wx.CheckBox( self, wx.ID_ANY, u"Master", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.master_chk, 0, wx.ALL, 5 )
		
		self.system_chk = wx.CheckBox( self, wx.ID_ANY, u"System", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.system_chk, 0, wx.ALL, 5 )
		
		
		sbSizer3.Add( gSizer1, 0, wx.EXPAND, 5 )
		
		
		bSizer10.Add( sbSizer3, 0, wx.EXPAND|wx.ALL, 5 )
		
		m_sdbSizer3 = wx.StdDialogButtonSizer()
		self.m_sdbSizer3OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer3.AddButton( self.m_sdbSizer3OK )
		self.m_sdbSizer3Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer3.AddButton( self.m_sdbSizer3Cancel )
		m_sdbSizer3.Realize();
		
		bSizer10.Add( m_sdbSizer3, 1, wx.EXPAND|wx.ALL, 5 )
		
		
		self.SetSizer( bSizer10 )
		self.Layout()
		bSizer10.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_sdbSizer3Cancel.Bind( wx.EVT_BUTTON, self.on_cancel )
		self.m_sdbSizer3OK.Bind( wx.EVT_BUTTON, self.on_ok )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_cancel( self, event ):
		event.Skip()
	
	def on_ok( self, event ):
		event.Skip()
	

###########################################################################
## Class MultiPing
###########################################################################

class MultiPing ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 730,300 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.olv_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.olv_sizer = wx.BoxSizer( wx.VERTICAL )
		
		
		self.olv_panel.SetSizer( self.olv_sizer )
		self.olv_panel.Layout()
		self.olv_sizer.Fit( self.olv_panel )
		bSizer4.Add( self.olv_panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer4 )
		self.Layout()
		self.rc_menu = wx.Menu()
		self.m_menuItem37 = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"Show Details", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.m_menuItem37 )
		
		self.Bind( wx.EVT_RIGHT_DOWN, self.MultiPingOnContextMenu ) 
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_MENU, self.on_show_details, id = self.m_menuItem37.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_show_details( self, event ):
		event.Skip()
	
	def MultiPingOnContextMenu( self, event ):
		self.PopupMenu( self.rc_menu, event.GetPosition() )
		

###########################################################################
## Class DeviceConfiguration
###########################################################################

class DeviceConfiguration ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Device Settings", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer13 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Hostname", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer14.Add( self.m_staticText3, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.hostname_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		bSizer14.Add( self.hostname_txt, 0, wx.ALL, 5 )
		
		
		bSizer13.Add( bSizer14, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 5 )
		
		sbSizer7 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, wx.EmptyString ), wx.HORIZONTAL )
		
		self.dhcp_chk = wx.RadioButton( self, wx.ID_ANY, u"DHCP", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
		sbSizer7.Add( self.dhcp_chk, 0, wx.ALL, 5 )
		
		self.static_chk = wx.RadioButton( self, wx.ID_ANY, u"Static", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
		sbSizer7.Add( self.static_chk, 0, wx.ALL, 5 )
		
		
		bSizer13.Add( sbSizer7, 0, wx.EXPAND, 5 )
		
		sbSizer5 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"IP settings" ), wx.VERTICAL )
		
		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"IP Address", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		bSizer17.Add( self.m_staticText4, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.ip_address_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		bSizer17.Add( self.ip_address_txt, 0, wx.ALL, 5 )
		
		
		sbSizer5.Add( bSizer17, 1, wx.EXPAND, 5 )
		
		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Subnet Mask", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		bSizer18.Add( self.m_staticText5, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.subnet_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		bSizer18.Add( self.subnet_txt, 0, wx.ALL, 5 )
		
		
		sbSizer5.Add( bSizer18, 1, wx.EXPAND, 5 )
		
		bSizer19 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Gateway IP", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		bSizer19.Add( self.m_staticText6, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.gateway_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		bSizer19.Add( self.gateway_txt, 0, wx.ALL, 5 )
		
		
		sbSizer5.Add( bSizer19, 1, wx.EXPAND, 5 )
		
		
		bSizer13.Add( sbSizer5, 1, wx.EXPAND|wx.ALL, 5 )
		
		sbSizer6 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Master Info" ), wx.VERTICAL )
		
		bSizer20 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Master Address", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		bSizer20.Add( self.m_staticText7, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.master_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		bSizer20.Add( self.master_txt, 0, wx.ALL, 5 )
		
		
		sbSizer6.Add( bSizer20, 1, wx.EXPAND, 5 )
		
		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Device Number", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		bSizer21.Add( self.m_staticText8, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.device_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		bSizer21.Add( self.device_txt, 0, wx.ALL, 5 )
		
		
		sbSizer6.Add( bSizer21, 1, wx.EXPAND, 5 )
		
		
		bSizer13.Add( sbSizer6, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button1 = wx.Button( self, wx.ID_ANY, u"Set", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer16.Add( self.m_button1, 0, wx.ALL, 5 )
		
		self.m_button2 = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer16.Add( self.m_button2, 0, wx.ALL, 5 )
		
		self.m_button3 = wx.Button( self, wx.ID_ANY, u"Abort", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer16.Add( self.m_button3, 0, wx.ALL, 5 )
		
		
		bSizer13.Add( bSizer16, 0, wx.ALL, 5 )
		
		
		self.SetSizer( bSizer13 )
		self.Layout()
		bSizer13.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.on_cancel )
		self.m_button1.Bind( wx.EVT_BUTTON, self.on_set )
		self.m_button2.Bind( wx.EVT_BUTTON, self.on_cancel )
		self.m_button3.Bind( wx.EVT_BUTTON, self.on_abort )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_cancel( self, event ):
		event.Skip()
	
	def on_set( self, event ):
		event.Skip()
	
	
	def on_abort( self, event ):
		event.Skip()
	

