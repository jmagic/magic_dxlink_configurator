from distutils.core import setup
import py2exe
import matplotlib

      
setup( options={'py2exe': { 'excludes': ['_gtkagg','_tkagg','_agg2','_cairo','_cocoaagg' ,'_fltkagg','_gtk','_gtkcairo','backend_qt','backend_qt4','backend_qt4agg','backend_qtagg','backend_cairo','backend_cocoaagg','Tkconstants','Tkinter','tcl',"_imagingtk","PIL._imagingtk","ImageTk","PIL.ImageTk" ,'FixTk','_gtkagg', '_tkagg', '_agg2',
                                         '_cairo', '_cocoaagg', '_fltkagg', '_gtk',
                                         '_tkinter','_gtkcairo',]}},


    windows= [
    {
        "script" : "Magic_DXLink_Configurator.py",
        "icon_resources": [(1, "icon/MDC_icon.ico") ]
        }
        ],
        data_files=matplotlib.get_py2exe_datafiles())
