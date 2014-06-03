
# Copyright (C) 2014 LiuLang <gsushzhsosgsu@gmail.com>
# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

from gi.repository import GLib
from gi.repository import Gtk

from bcloud import Config
_ = Config._


class PreferencesDialog(Gtk.Dialog):

    def __init__(self, app):
        self.app = app
        super().__init__(
                _('Preferences'), app.window, Gtk.DialogFlags.MODAL,
                (Gtk.STOCK_CLOSE, Gtk.ResponseType.OK))
        self.set_default_response(Gtk.ResponseType.OK)

        self.set_default_size(480, 360)
        self.set_border_width(10)

        box = self.get_content_area()

        notebook = Gtk.Notebook()
        box.pack_start(notebook, True, True, 0)

        # General Tab
        general_grid = Gtk.Grid()
        general_grid.props.halign = Gtk.Align.CENTER
        general_grid.props.column_spacing = 12
        general_grid.props.row_spacing = 5
        general_grid.props.margin_top = 5
        notebook.append_page(general_grid, Gtk.Label.new(_('General')))

        dir_label = Gtk.Label.new(_('Save To:'))
        dir_label.props.xalign = 1
        general_grid.attach(dir_label, 0, 0, 1, 1)
        dir_button = Gtk.FileChooserButton()
        dir_button.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        dir_button.set_current_folder(app.profile['save-dir'])
        dir_button.connect('file-set', self.on_dir_update)
        general_grid.attach(dir_button, 1, 0, 1, 1)

        concurr_label = Gtk.Label.new(_('Concurrent downloads:'))
        concurr_label.props.xalign = 1
        general_grid.attach(concurr_label, 0, 1, 1, 1)
        concurr_spin = Gtk.SpinButton.new_with_range(1, 5, 1)
        concurr_spin.set_value(self.app.profile['concurr-tasks'])
        concurr_spin.props.halign = Gtk.Align.START
        concurr_spin.connect('value-changed', self.on_concurr_value_changed)
        general_grid.attach(concurr_spin, 1, 1, 1, 1)

        upload_hidden_label = Gtk.Label.new(_('Upload hidden files:'))
        upload_hidden_label.props.xalign = 1
        general_grid.attach(upload_hidden_label, 0, 2, 1, 1)
        upload_hidden_switch = Gtk.Switch()
        upload_hidden_switch.props.halign = Gtk.Align.START
        upload_hidden_switch.set_tooltip_text(
                _('Also upload hidden files and folders'))
        upload_hidden_switch.set_active(
                self.app.profile['upload-hidden-files'])
        upload_hidden_switch.connect(
                'notify::active', self.on_upload_hidden_switch_activate)
        general_grid.attach(upload_hidden_switch, 1, 2, 1, 1)

        notify_label = Gtk.Label.new(_('Use notification:'))
        notify_label.props.xalign = 1
        general_grid.attach(notify_label, 0, 3, 1, 1)
        notify_switch = Gtk.Switch()
        notify_switch.props.halign = Gtk.Align.START
        notify_switch.set_active(self.app.profile['use-notify'])
        notify_switch.connect(
                'notify::active', self.on_notify_switch_activate)
        general_grid.attach(notify_switch, 1, 3, 1, 1)

        dark_theme_label = Gtk.Label.new(_('Use dark theme:'))
        dark_theme_label.props.xalign = 1
        general_grid.attach(dark_theme_label, 0, 4, 1, 1)
        dark_theme_switch = Gtk.Switch()
        dark_theme_switch.set_active(self.app.profile['use-dark-theme'])
        dark_theme_switch.connect(
                'notify::active', self.on_dark_theme_switch_toggled)
        dark_theme_switch.props.halign = Gtk.Align.START
        general_grid.attach(dark_theme_switch, 1, 4, 1, 1)

        status_label = Gtk.Label.new(_('Minimize to system tray:'))
        status_label.props.xalign = 1
        general_grid.attach(status_label, 0, 5, 1, 1)
        status_switch = Gtk.Switch()
        status_switch.set_active(self.app.profile['use-status-icon'])
        status_switch.connect(
                'notify::active', self.on_status_switch_activate)
        status_switch.props.halign = Gtk.Align.START
        general_grid.attach(status_switch, 1, 5, 1, 1)

        stream_label = Gtk.Label.new(_('Use streaming mode:'))
        stream_label.props.xalign = 1
        general_grid.attach(stream_label, 0, 6, 1, 1)
        stream_switch = Gtk.Switch()
        stream_switch.set_active(self.app.profile['use-streaming'])
        stream_switch.connect(
                'notify::active', self.on_stream_switch_activate)
        stream_switch.props.halign = Gtk.Align.START
        stream_switch.set_tooltip_text(_('When opening a video file, try to download a m3u8 playlist, instread of getting its file source link'))
        general_grid.attach(stream_switch, 1, 6, 1, 1)

        box.show_all()

    def on_dir_update(self, file_button):
        dir_name = file_button.get_filename()
        if dir_name:
            self.app.profile['save-dir'] = dir_name

    def on_concurr_value_changed(self, concurr_spin):
        self.app.profile['concurr-tasks'] = concurr_spin.get_value()

    def on_upload_hidden_switch_activate(self, switch, event):
        self.app.profile['upload-hidden-files'] = switch.get_active()

    def on_notify_switch_activate(self, switch, event):
        self.app.profile['use-notify'] = switch.get_active()

    def on_dark_theme_switch_toggled(self, switch, event):
        self.app.profile['use-dark-theme'] = switch.get_active()

    def on_status_switch_activate(self, switch, event):
        self.app.profile['use-status-icon'] = switch.get_active()

    def on_stream_switch_activate(self, switch, event):
        self.app.profile['use-streaming'] = switch.get_active()
