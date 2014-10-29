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
		self.listenDHCP = wx.MenuItem( self.m_menu9, wx.ID_ANY, u"Listen for DHCP requests", wx.EmptyString, wx.ITEM_CHECK )
		self.m_menu9.AppendItem( self.listenDHCP )
		self.listenDHCP.Check( True )
		
		self.listenfilter = wx.MenuItem( self.m_menu9, wx.ID_ANY, u"Only show AMX devices", wx.EmptyString, wx.ITEM_CHECK )
		self.m_menu9.AppendItem( self.listenfilter )
		
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
		self.Bind( wx.EVT_MENU, self.toggle_dhcp_sniffing, id = self.listenDHCP.GetId() )
		self.Bind( wx.EVT_MENU, self.amx_only_filter, id = self.listenfilter.GetId() )
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
	
	def toggle_dhcp_sniffing( self, event ):
		event.Skip()
	
	def amx_only_filter( self, event ):
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
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

