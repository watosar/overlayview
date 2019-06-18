import appex
import photos
import lay_ui
import ui
      
body = ui.load_view()

#root = lay_ui.RootView(body=body)
root = lay_ui.root
lay_ui.present(body,ui.load_view_str((ui.dump_view(body))))
