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
		
		self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )
		
		self.olv_panel = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.olv_sizer = wx.BoxSizer( wx.VERTICAL )
		
		
		self.olv_panel.SetSizer( self.olv_sizer )
		self.olv_panel.Layout()
		self.olv_sizer.Fit( self.olv_panel )
		self.m_panel3 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.extra_sizer = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panel3.SetSizer( self.extra_sizer )
		self.m_panel3.Layout()
		self.extra_sizer.Fit( self.m_panel3 )
		self.m_splitter1.SplitVertically( self.olv_panel, self.m_panel3, 640 )
		bSizer2.Add( self.m_splitter1, 1, wx.EXPAND, 5 )
		
		
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
		
		self.listenfilter = wx.MenuItem( self.m_menu9, wx.ID_ANY, u"Only show AMX devices", wx.EmptyString, wx.ITEM_CHECK )
		self.m_menu9.AppendItem( self.listenfilter )
		
		self.m_menubar1.Append( self.m_menu9, u"Listen" ) 
		
		self.m_menu10 = wx.Menu()
		self.m_menubar1.Append( self.m_menu10, u"Delete" ) 
		
		self.m_menu111 = wx.Menu()
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
	
	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 640 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )
	
	def MainFrameOnContextMenu( self, event ):
		self.PopupMenu( self.rc_menu, event.GetPosition() )
		

