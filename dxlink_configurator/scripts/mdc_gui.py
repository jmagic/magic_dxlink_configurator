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
		self.file_menu = wx.Menu()
		self.import_menu = wx.Menu()
		self.import_csv_menu = wx.MenuItem( self.import_menu, wx.ID_ANY, u"Import from a CSV", wx.EmptyString, wx.ITEM_NORMAL )
		self.import_menu.AppendItem( self.import_csv_menu )
		
		self.import_ip_menu = wx.MenuItem( self.import_menu, wx.ID_ANY, u"Import IP list", wx.EmptyString, wx.ITEM_NORMAL )
		self.import_menu.AppendItem( self.import_ip_menu )
		
		self.file_menu.AppendSubMenu( self.import_menu, u"Import" )
		
		self.export_menu = wx.Menu()
		self.export_csv_menu = wx.MenuItem( self.export_menu, wx.ID_ANY, u"Export to a CSV File", wx.EmptyString, wx.ITEM_NORMAL )
		self.export_menu.AppendItem( self.export_csv_menu )
		
		self.file_menu.AppendSubMenu( self.export_menu, u"Export" )
		
		self.quit_menu = wx.MenuItem( self.file_menu, wx.ID_ANY, u"Quit", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.AppendItem( self.quit_menu )
		
		self.m_menubar1.Append( self.file_menu, u"File" ) 
		
		self.edit_menu = wx.Menu()
		self.select_menu = wx.Menu()
		self.all_menu = wx.MenuItem( self.select_menu, wx.ID_ANY, u"Select All", wx.EmptyString, wx.ITEM_NORMAL )
		self.select_menu.AppendItem( self.all_menu )
		
		self.none_menu = wx.MenuItem( self.select_menu, wx.ID_ANY, u"Select None", wx.EmptyString, wx.ITEM_NORMAL )
		self.select_menu.AppendItem( self.none_menu )
		
		self.edit_menu.AppendSubMenu( self.select_menu, u"Select" )
		
		self.preferences_menu = wx.MenuItem( self.edit_menu, wx.ID_ANY, u"Preferences", wx.EmptyString, wx.ITEM_NORMAL )
		self.edit_menu.AppendItem( self.preferences_menu )
		
		self.m_menubar1.Append( self.edit_menu, u"Edit" ) 
		
		self.actions_menu = wx.Menu()
		self.update_device_menu = wx.MenuItem( self.actions_menu, wx.ID_ANY, u"Update Device Information", wx.EmptyString, wx.ITEM_NORMAL )
		self.actions_menu.AppendItem( self.update_device_menu )
		
		self.configure_menu = wx.MenuItem( self.actions_menu, wx.ID_ANY, u"Configure Device", wx.EmptyString, wx.ITEM_NORMAL )
		self.actions_menu.AppendItem( self.configure_menu )
		
		self.telnet_menu = wx.MenuItem( self.actions_menu, wx.ID_ANY, u"Telnet to Device", wx.EmptyString, wx.ITEM_NORMAL )
		self.actions_menu.AppendItem( self.telnet_menu )
		
		self.ssh_menu = wx.MenuItem( self.actions_menu, wx.ID_ANY, u"SSH to Device", wx.EmptyString, wx.ITEM_NORMAL )
		self.actions_menu.AppendItem( self.ssh_menu )
		
		self.send_menu = wx.MenuItem( self.actions_menu, wx.ID_ANY, u"Send Commands", wx.EmptyString, wx.ITEM_NORMAL )
		self.actions_menu.AppendItem( self.send_menu )
		
		self.reset_menu = wx.MenuItem( self.actions_menu, wx.ID_ANY, u"Reset Factory", wx.EmptyString, wx.ITEM_NORMAL )
		self.actions_menu.AppendItem( self.reset_menu )
		
		self.reboot_menu = wx.MenuItem( self.actions_menu, wx.ID_ANY, u"Reboot Device", wx.EmptyString, wx.ITEM_NORMAL )
		self.actions_menu.AppendItem( self.reboot_menu )
		
		self.m_menubar1.Append( self.actions_menu, u"Actions" ) 
		
		self.tools_menu = wx.Menu()
		self.ping_menu = wx.MenuItem( self.tools_menu, wx.ID_ANY, u"Ping Devices", wx.EmptyString, wx.ITEM_NORMAL )
		self.tools_menu.AppendItem( self.ping_menu )
		
		self.mse_menu = wx.MenuItem( self.tools_menu, wx.ID_ANY, u"MSE Baseline", wx.EmptyString, wx.ITEM_NORMAL )
		self.tools_menu.AppendItem( self.mse_menu )
		
		self.add_menu = wx.MenuItem( self.tools_menu, wx.ID_ANY, u"Add line item", wx.EmptyString, wx.ITEM_NORMAL )
		self.tools_menu.AppendItem( self.add_menu )
		
		self.generate_menu = wx.MenuItem( self.tools_menu, wx.ID_ANY, u"Generate IP List", wx.EmptyString, wx.ITEM_NORMAL )
		self.tools_menu.AppendItem( self.generate_menu )
		
		self.generate_dgx_menu = wx.MenuItem( self.tools_menu, wx.ID_ANY, u"Generate DGX List", wx.EmptyString, wx.ITEM_NORMAL )
		self.tools_menu.AppendItem( self.generate_dgx_menu )
		
		self.m_menubar1.Append( self.tools_menu, u"Tools" ) 
		
		self.identify_menu = wx.Menu()
		self.led_on_menu = wx.MenuItem( self.identify_menu, wx.ID_ANY, u"Turn on LED's", wx.EmptyString, wx.ITEM_NORMAL )
		self.identify_menu.AppendItem( self.led_on_menu )
		
		self.led_off_menu = wx.MenuItem( self.identify_menu, wx.ID_ANY, u"Turn off LED's", wx.EmptyString, wx.ITEM_NORMAL )
		self.identify_menu.AppendItem( self.led_off_menu )
		
		self.m_menubar1.Append( self.identify_menu, u"Identify" ) 
		
		self.listen_menu = wx.Menu()
		self.dhcp_sniffing_chk = wx.MenuItem( self.listen_menu, wx.ID_ANY, u"Listen for DHCP requests", wx.EmptyString, wx.ITEM_CHECK )
		self.listen_menu.AppendItem( self.dhcp_sniffing_chk )
		self.dhcp_sniffing_chk.Check( True )
		
		self.amx_only_filter_chk = wx.MenuItem( self.listen_menu, wx.ID_ANY, u"Only add AMX devices", wx.EmptyString, wx.ITEM_CHECK )
		self.listen_menu.AppendItem( self.amx_only_filter_chk )
		
		self.m_menubar1.Append( self.listen_menu, u"Listen" ) 
		
		self.delete_menu = wx.Menu()
		self.delete_item_menu = wx.MenuItem( self.delete_menu, wx.ID_ANY, u"Delete Item", wx.EmptyString, wx.ITEM_NORMAL )
		self.delete_menu.AppendItem( self.delete_item_menu )
		
		self.delete_all_menu = wx.MenuItem( self.delete_menu, wx.ID_ANY, u"Delete All Items", wx.EmptyString, wx.ITEM_NORMAL )
		self.delete_menu.AppendItem( self.delete_all_menu )
		
		self.m_menubar1.Append( self.delete_menu, u"Delete" ) 
		
		self.help_menu = wx.Menu()
		self.about_menu = wx.MenuItem( self.help_menu, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
		self.help_menu.AppendItem( self.about_menu )
		
		self.m_menubar1.Append( self.help_menu, u"Help" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		self.status_bar = self.CreateStatusBar( 2, wx.ST_SIZEGRIP, wx.ID_ANY )
		self.rc_menu = wx.Menu()
		self.update_rc_menu = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"Update device information", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.update_rc_menu )
		
		self.configure__rc_menu = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"Configure Device", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.configure__rc_menu )
		
		self.ping_rc_menu = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"Ping Device", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.ping_rc_menu )
		
		self.send_rc_menu = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"Send Commands", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.send_rc_menu )
		
		self.reset_rc_menu = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"Reset Factory", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.reset_rc_menu )
		
		self.delete_rc_menu = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"Delete", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.delete_rc_menu )
		
		self.telnet_rc_menu = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"Telnet to Device", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.telnet_rc_menu )
		
		self.factory_rc_menu = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"FactoryAV", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.factory_rc_menu )
		
		self.reboot_rc_menu = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"Reboot Device", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.reboot_rc_menu )
		
		self.mse_rc_menu = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"MSE Baseline", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.mse_rc_menu )
		
		self.browser_rc_menu = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"Open device in webbrowser", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.browser_rc_menu )
		
		self.Bind( wx.EVT_RIGHT_DOWN, self.MainFrameOnContextMenu ) 
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.on_close )
		self.Bind( wx.EVT_MENU, self.import_csv_file, id = self.import_csv_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.import_ip_list, id = self.import_ip_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.export_to_csv, id = self.export_csv_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.on_quit, id = self.quit_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.on_select_all, id = self.all_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.on_select_none, id = self.none_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.configure_prefs, id = self.preferences_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.update_device_information, id = self.update_device_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.configure_device, id = self.configure_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.telnet_to, id = self.telnet_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.ssh_to, id = self.ssh_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.send_commands, id = self.send_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.reset_factory, id = self.reset_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.reboot, id = self.reboot_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.multi_ping, id = self.ping_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.mse_baseline, id = self.mse_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.add_line, id = self.add_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.generate_list, id = self.generate_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.generate_dgx_list, id = self.generate_dgx_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.turn_on_leds, id = self.led_on_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.turn_off_leds, id = self.led_off_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.on_dhcp_sniffing, id = self.dhcp_sniffing_chk.GetId() )
		self.Bind( wx.EVT_MENU, self.on_amx_only_filter, id = self.amx_only_filter_chk.GetId() )
		self.Bind( wx.EVT_MENU, self.on_delete_item, id = self.delete_item_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.delete_all_items, id = self.delete_all_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.on_about_box, id = self.about_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.update_device_information, id = self.update_rc_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.configure_device, id = self.configure__rc_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.multi_ping, id = self.ping_rc_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.send_commands, id = self.send_rc_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.reset_factory, id = self.reset_rc_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.delete_item, id = self.delete_rc_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.telnet_to, id = self.telnet_rc_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.factory_av, id = self.factory_rc_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.reboot, id = self.reboot_rc_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.mse_baseline, id = self.mse_rc_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.open_url, id = self.browser_rc_menu.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_close( self, event ):
		event.Skip()
	
	def import_csv_file( self, event ):
		event.Skip()
	
	def import_ip_list( self, event ):
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
	
	def update_device_information( self, event ):
		event.Skip()
	
	def configure_device( self, event ):
		event.Skip()
	
	def telnet_to( self, event ):
		event.Skip()
	
	def ssh_to( self, event ):
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
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Default Master Address", wx.DefaultPosition, wx.DefaultSize, 0 )
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
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Default Device Number", wx.DefaultPosition, wx.DefaultSize, 0 )
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
		
		self.sounds_chk = wx.CheckBox( self, wx.ID_ANY, u"Play Sounds", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer2.Add( self.sounds_chk, 0, wx.ALL, 5 )
		
		
		bSizer10.Add( sbSizer2, 0, wx.EXPAND|wx.ALL, 5 )
		
		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Columns To Display" ), wx.VERTICAL )
		
		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.model_chk = wx.CheckBox( self, wx.ID_ANY, u"Model", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.model_chk, 0, wx.ALL, 5 )
		
		self.mac_chk = wx.CheckBox( self, wx.ID_ANY, u"MAC", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.mac_chk, 0, wx.ALL, 5 )
		
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
		
		bSizer44 = wx.BoxSizer( wx.VERTICAL )
		
		self.olv_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.olv_sizer = wx.BoxSizer( wx.VERTICAL )
		
		
		self.olv_panel.SetSizer( self.olv_sizer )
		self.olv_panel.Layout()
		self.olv_sizer.Fit( self.olv_panel )
		bSizer44.Add( self.olv_panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer44, 1, wx.EXPAND, 5 )
		
		bSizer45 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer8 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Logging" ), wx.VERTICAL )
		
		self.log_enable_chk = wx.CheckBox( self, wx.ID_ANY, u"Log to file", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer8.Add( self.log_enable_chk, 0, wx.ALL, 5 )
		
		self.log_file_txt = wx.StaticText( self, wx.ID_ANY, u"logfile", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.log_file_txt.Wrap( -1 )
		sbSizer8.Add( self.log_file_txt, 0, wx.ALL, 5 )
		
		
		bSizer45.Add( sbSizer8, 0, wx.EXPAND, 5 )
		
		
		bSizer4.Add( bSizer45, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer4 )
		self.Layout()
		self.rc_menu = wx.Menu()
		self.m_menuItem37 = wx.MenuItem( self.rc_menu, wx.ID_ANY, u"Show Details", wx.EmptyString, wx.ITEM_NORMAL )
		self.rc_menu.AppendItem( self.m_menuItem37 )
		
		self.Bind( wx.EVT_RIGHT_DOWN, self.MultiPingOnContextMenu ) 
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.log_enable_chk.Bind( wx.EVT_CHECKBOX, self.on_log_enable )
		self.Bind( wx.EVT_MENU, self.on_show_details, id = self.m_menuItem37.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_log_enable( self, event ):
		event.Skip()
	
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
		
		self.static_chk = wx.RadioButton( self, wx.ID_ANY, u"Static", wx.DefaultPosition, wx.DefaultSize, 0 )
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
		self.dhcp_chk.Bind( wx.EVT_RADIOBUTTON, self.on_dhcp )
		self.static_chk.Bind( wx.EVT_RADIOBUTTON, self.on_dhcp )
		self.m_button1.Bind( wx.EVT_BUTTON, self.on_set )
		self.m_button2.Bind( wx.EVT_BUTTON, self.on_cancel )
		self.m_button3.Bind( wx.EVT_BUTTON, self.on_abort )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_cancel( self, event ):
		event.Skip()
	
	def on_dhcp( self, event ):
		event.Skip()
	
	
	def on_set( self, event ):
		event.Skip()
	
	
	def on_abort( self, event ):
		event.Skip()
	

###########################################################################
## Class GenerateIP
###########################################################################

class GenerateIP ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Generate IP list", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer27 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel4 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer28 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer29 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText9 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Starting IP", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText9.Wrap( -1 )
		bSizer29.Add( self.m_staticText9, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.start_txt = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.start_txt.SetMinSize( wx.Size( 200,-1 ) )
		
		bSizer29.Add( self.start_txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer28.Add( bSizer29, 1, wx.EXPAND, 5 )
		
		bSizer30 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText10 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Finishing IP", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText10.Wrap( -1 )
		bSizer30.Add( self.m_staticText10, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.finish_txt = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.finish_txt.SetMinSize( wx.Size( 200,-1 ) )
		
		bSizer30.Add( self.finish_txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer28.Add( bSizer30, 1, wx.EXPAND, 5 )
		
		bSizer31 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button5 = wx.Button( self.m_panel4, wx.ID_ANY, u"Replace List", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer31.Add( self.m_button5, 0, wx.ALL, 5 )
		
		self.m_button6 = wx.Button( self.m_panel4, wx.ID_ANY, u"Add to List", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer31.Add( self.m_button6, 0, wx.ALL, 5 )
		
		self.m_button7 = wx.Button( self.m_panel4, wx.ID_ANY, u"Save as File", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer31.Add( self.m_button7, 0, wx.ALL, 5 )
		
		
		bSizer28.Add( bSizer31, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.m_panel4.SetSizer( bSizer28 )
		self.m_panel4.Layout()
		bSizer28.Fit( self.m_panel4 )
		bSizer27.Add( self.m_panel4, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer27 )
		self.Layout()
		bSizer27.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button5.Bind( wx.EVT_BUTTON, self.on_replace )
		self.m_button6.Bind( wx.EVT_BUTTON, self.on_add )
		self.m_button7.Bind( wx.EVT_BUTTON, self.on_save )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_replace( self, event ):
		event.Skip()
	
	def on_add( self, event ):
		event.Skip()
	
	def on_save( self, event ):
		event.Skip()
	

###########################################################################
## Class MultiSend
###########################################################################

class MultiSend ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Multiple Send Command", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer32 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer32.SetMinSize( wx.Size( 740,550 ) ) 
		self.m_panel5 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer33 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer34 = wx.BoxSizer( wx.VERTICAL )
		
		self.olv_panel = wx.Panel( self.m_panel5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.olv_sizer = wx.BoxSizer( wx.VERTICAL )
		
		
		self.olv_panel.SetSizer( self.olv_sizer )
		self.olv_panel.Layout()
		self.olv_sizer.Fit( self.olv_panel )
		bSizer34.Add( self.olv_panel, 1, wx.EXPAND, 5 )
		
		
		bSizer33.Add( bSizer34, 1, wx.EXPAND, 5 )
		
		bSizer36 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer7 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel5, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )
		
		bSizer38 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.query_chk = wx.RadioButton( self.m_panel5, wx.ID_ANY, u"Query", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
		self.query_chk.SetValue( True ) 
		bSizer38.Add( self.query_chk, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.command_chk = wx.RadioButton( self.m_panel5, wx.ID_ANY, u"Command", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer38.Add( self.command_chk, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		commands_cmbChoices = []
		self.commands_cmb = wx.ComboBox( self.m_panel5, wx.ID_ANY, u"Commands", wx.DefaultPosition, wx.DefaultSize, commands_cmbChoices, 0 )
		self.commands_cmb.SetMinSize( wx.Size( 180,-1 ) )
		
		bSizer38.Add( self.commands_cmb, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		action_cmbChoices = []
		self.action_cmb = wx.ComboBox( self.m_panel5, wx.ID_ANY, u"Actions", wx.DefaultPosition, wx.DefaultSize, action_cmbChoices, 0 )
		bSizer38.Add( self.action_cmb, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.get_all_chk = wx.CheckBox( self.m_panel5, wx.ID_ANY, u"Send All Query's", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer38.Add( self.get_all_chk, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		sbSizer7.Add( bSizer38, 1, wx.EXPAND, 5 )
		
		bSizer40 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer41 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText11 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"send_command <DEVICE>:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		bSizer41.Add( self.m_staticText11, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )
		
		self.string_port_txt = wx.TextCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 20,-1 ), 0 )
		bSizer41.Add( self.string_port_txt, 0, wx.TOP|wx.BOTTOM, 5 )
		
		self.m_staticText12 = wx.StaticText( self.m_panel5, wx.ID_ANY, u":<SYSTEM>, \"'", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		bSizer41.Add( self.m_staticText12, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.RIGHT, 5 )
		
		self.string_command_txt = wx.TextCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.string_command_txt.SetMinSize( wx.Size( 240,-1 ) )
		
		bSizer41.Add( self.string_command_txt, 0, wx.ALL, 5 )
		
		self.m_staticText13 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"'\"", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		bSizer41.Add( self.m_staticText13, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM|wx.RIGHT, 5 )
		
		
		bSizer40.Add( bSizer41, 1, wx.EXPAND, 5 )
		
		bSizer42 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.send_btn = wx.Button( self.m_panel5, wx.ID_ANY, u"Send", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer42.Add( self.send_btn, 0, wx.ALL, 5 )
		
		self.exit_btn = wx.Button( self.m_panel5, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer42.Add( self.exit_btn, 0, wx.ALL, 5 )
		
		
		bSizer40.Add( bSizer42, 0, wx.EXPAND, 5 )
		
		
		sbSizer7.Add( bSizer40, 0, wx.EXPAND, 5 )
		
		
		bSizer36.Add( sbSizer7, 1, wx.EXPAND|wx.ALL, 5 )
		
		
		bSizer33.Add( bSizer36, 0, wx.EXPAND, 5 )
		
		bSizer37 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.description_txt = wx.TextCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.HSCROLL|wx.TE_MULTILINE )
		self.description_txt.SetMinSize( wx.Size( 206,-1 ) )
		
		bSizer37.Add( self.description_txt, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.syntax_txt = wx.TextCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,200 ), wx.HSCROLL|wx.TE_MULTILINE )
		bSizer37.Add( self.syntax_txt, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer33.Add( bSizer37, 0, wx.EXPAND, 5 )
		
		
		self.m_panel5.SetSizer( bSizer33 )
		self.m_panel5.Layout()
		bSizer33.Fit( self.m_panel5 )
		bSizer32.Add( self.m_panel5, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer32 )
		self.Layout()
		bSizer32.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.query_chk.Bind( wx.EVT_RADIOBUTTON, self.on_query )
		self.command_chk.Bind( wx.EVT_RADIOBUTTON, self.on_query )
		self.commands_cmb.Bind( wx.EVT_COMBOBOX, self.on_command_combo )
		self.action_cmb.Bind( wx.EVT_COMBOBOX, self.on_action_combo )
		self.get_all_chk.Bind( wx.EVT_CHECKBOX, self.on_get_all )
		self.send_btn.Bind( wx.EVT_BUTTON, self.on_send )
		self.exit_btn.Bind( wx.EVT_BUTTON, self.on_exit )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_query( self, event ):
		event.Skip()
	
	
	def on_command_combo( self, event ):
		event.Skip()
	
	def on_action_combo( self, event ):
		event.Skip()
	
	def on_get_all( self, event ):
		event.Skip()
	
	def on_send( self, event ):
		event.Skip()
	
	def on_exit( self, event ):
		event.Skip()
	

###########################################################################
## Class ProgressDialog
###########################################################################

class ProgressDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Progress", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer42 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel7 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer43 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_gauge1 = wx.Gauge( self.m_panel7, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge1.SetValue( 0 ) 
		bSizer43.Add( self.m_gauge1, 0, wx.ALL, 5 )
		
		
		self.m_panel7.SetSizer( bSizer43 )
		self.m_panel7.Layout()
		bSizer43.Fit( self.m_panel7 )
		bSizer42.Add( self.m_panel7, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer42 )
		self.Layout()
		bSizer42.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

