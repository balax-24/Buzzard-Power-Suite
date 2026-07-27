"""Buzzard GTK Desktop Control Center & System Tray Application.

Provides an interactive GTK3 Control Center window with live power draw telemetry (W),
battery health metrics, one-click profile switching, hardware controls (80% charge limit,
refresh rate switching), plus an AppIndicator system tray icon.
"""

from pathlib import Path
import sys
from buzzard.managers import BatteryManager, DisplayManager, PowerEstimator, VendorManager
from buzzard.services.diagnostic_service import DiagnosticService
from buzzard.services.profile_service import ProfileService
from buzzard.services.status_service import StatusService

try:
    import gi
    gi.require_version("Gtk", "3.0")
    gi.require_version("GdkPixbuf", "2.0")
    try:
        gi.require_version("AppIndicator3", "0.1")
        from gi.repository import AppIndicator3 as appindicator
    except Exception:
        try:
            gi.require_version("AyatanaAppIndicator3", "0.1")
            from gi.repository import AyatanaAppIndicator3 as appindicator
        except Exception:
            appindicator = None
    try:
        gi.require_version("Notify", "0.7")
        from gi.repository import Notify
        Notify.init("Buzzard Power Suite")
    except Exception:
        Notify = None

    from gi.repository import GdkPixbuf, GLib, Gtk
except ImportError:
    Gtk = None
    appindicator = None
    Notify = None

ICON_PATH = Path(__file__).parent.parent / "assets" / "buzzard.png"


class BuzzardControlWindow(Gtk.Window):
    """Buzzard Power Suite Desktop Control Center Window."""

    def __init__(self, tray_app: any = None) -> None:
        super().__init__(title="🦅 Buzzard Power Suite - Control Center")
        self.tray_app = tray_app
        self.set_default_size(480, 560)
        self.set_position(Gtk.WindowPosition.CENTER)

        if ICON_PATH.exists():
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(str(ICON_PATH.resolve()), 64, 64, True)
                self.set_icon(pixbuf)
            except Exception:
                pass

        # Main Box Layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        main_box.set_margin_start(16)
        main_box.set_margin_end(16)
        main_box.set_margin_top(16)
        main_box.set_margin_bottom(16)
        self.add(main_box)

        # 1. Header Banner Box
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        if ICON_PATH.exists():
            try:
                img_pix = GdkPixbuf.Pixbuf.new_from_file_at_scale(str(ICON_PATH.resolve()), 48, 48, True)
                image = Gtk.Image.new_from_pixbuf(img_pix)
                header_box.pack_start(image, False, False, 0)
            except Exception:
                pass

        title_lbl = Gtk.Label()
        title_lbl.set_markup("<b><big>Buzzard Power Suite</big></b>\n<small>Universal Linux Power & AI Adaptive Suite</small>")
        title_lbl.set_xalign(0)
        header_box.pack_start(title_lbl, True, True, 0)
        main_box.pack_start(header_box, False, False, 0)

        main_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 0)

        # 2. Telemetry Status Card (Frame)
        frame = Gtk.Frame(label=" ⚡ Real-Time Power Telemetry ")
        telemetry_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        telemetry_box.set_margin_start(12)
        telemetry_box.set_margin_end(12)
        telemetry_box.set_margin_top(10)
        telemetry_box.set_margin_bottom(10)
        frame.add(telemetry_box)

        self.lbl_profile = Gtk.Label(label="Active Profile: Loading...")
        self.lbl_profile.set_xalign(0)
        telemetry_box.pack_start(self.lbl_profile, False, False, 0)

        self.lbl_power = Gtk.Label(label="Power Draw: Calculating...")
        self.lbl_power.set_xalign(0)
        telemetry_box.pack_start(self.lbl_power, False, False, 0)

        self.lbl_battery = Gtk.Label(label="Battery: Reading sysfs...")
        self.lbl_battery.set_xalign(0)
        telemetry_box.pack_start(self.lbl_battery, False, False, 0)

        main_box.pack_start(frame, False, False, 0)

        # 3. Profiles Selection Grid
        prof_frame = Gtk.Frame(label=" ⚡ Select Power Profile ")
        grid = Gtk.Grid()
        grid.set_column_spacing(8)
        grid.set_row_spacing(8)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        prof_frame.add(grid)

        profiles = [
            ("macmode", "🍏 MacMode (~4W)", 0, 0),
            ("low", "🔋 Low Power", 0, 1),
            ("hybrid", "⚖️ Hybrid", 1, 0),
            ("full", "⚡ Full Power", 1, 1),
            ("gaming", "🎮 Gaming", 2, 0),
            ("creator", "🎨 Creator", 2, 1),
            ("travel", "✈️ Travel", 3, 0),
            ("meeting", "🤝 Meeting", 3, 1),
            ("auto", "🤖 Auto Mode", 4, 0),
        ]

        for p_key, p_label, r, c in profiles:
            btn = Gtk.Button(label=p_label)
            btn.connect("clicked", self.on_profile_click, p_key)
            grid.attach(btn, c, r, 1, 1)

        main_box.pack_start(prof_frame, False, False, 0)

        # 4. Quick Hardware Controls
        ctrl_frame = Gtk.Frame(label=" ⚙️ Quick Hardware Controls ")
        ctrl_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        ctrl_box.set_margin_start(10)
        ctrl_box.set_margin_end(10)
        ctrl_box.set_margin_top(10)
        ctrl_box.set_margin_bottom(10)
        ctrl_frame.add(ctrl_box)

        btn_80 = Gtk.Button(label="🔋 Limit 80%")
        btn_80.connect("clicked", lambda w: VendorManager.apply_vendor_settings({"battery_charge_limit": 80}))
        ctrl_box.pack_start(btn_80, True, True, 0)

        btn_100 = Gtk.Button(label="🔋 Full 100%")
        btn_100.connect("clicked", lambda w: VendorManager.apply_vendor_settings({"battery_charge_limit": 100}))
        ctrl_box.pack_start(btn_100, True, True, 0)

        btn_60 = Gtk.Button(label="🖥️ 60Hz")
        btn_60.connect("clicked", lambda w: DisplayManager.set_refresh_rate(60))
        ctrl_box.pack_start(btn_60, True, True, 0)

        btn_144 = Gtk.Button(label="🖥️ High Hz")
        btn_144.connect("clicked", lambda w: DisplayManager.set_refresh_rate(144))
        ctrl_box.pack_start(btn_144, True, True, 0)

        main_box.pack_start(ctrl_frame, False, False, 0)

        # 5. Footer Diagnostics & System Tray Minimizer
        footer_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        btn_doc = Gtk.Button(label="🩺 Run Doctor Diagnostics")
        btn_doc.connect("clicked", self.on_doctor_click)
        footer_box.pack_start(btn_doc, True, True, 0)

        btn_tray = Gtk.Button(label="📥 Minimize to Tray")
        btn_tray.connect("clicked", lambda w: self.hide())
        footer_box.pack_start(btn_tray, True, True, 0)

        main_box.pack_start(footer_box, False, False, 0)

        self.connect("delete-event", lambda w, e: self.hide_on_delete())
        self.refresh_telemetry()
        GLib.timeout_add_seconds(3, self.refresh_telemetry)

    def refresh_telemetry(self) -> bool:
        """Refreshes live GUI window telemetry."""
        try:
            status = StatusService.get_status()
            est = PowerEstimator.estimate()
            wattage_str = f"{est['power_draw_w']:.2f} W" if est['power_draw_w'] > 0 else "AC Connected"
            runtime_str = est.get("estimated_runtime", f"{est.get('hours_remaining', 0)}h")

            self.lbl_profile.set_markup(f"<b>Active Profile:</b> <span foreground='#00AAFF'>{status['profile'].upper()}</span> ({status['vendor_name']})")
            self.lbl_power.set_markup(f"<b>Live Wattage Draw:</b> <span foreground='#FFD700'>{wattage_str}</span> (Runtime: {runtime_str})")
            self.lbl_battery.set_markup(f"<b>Battery Capacity:</b> {status['battery_percent']}% ({status['battery_status']}), AC: {status['ac_connected']}")

            if self.tray_app:
                self.tray_app.refresh_telemetry()
        except Exception:
            pass
        return True

    def on_profile_click(self, widget, profile_name: str) -> None:
        ProfileService.apply_profile(profile_name)
        self.refresh_telemetry()

    def on_doctor_click(self, widget) -> None:
        report = DiagnosticService.report()
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="🦅 Buzzard System Doctor Diagnostics",
        )
        msg_lines = [f"• {k}: {v}" for k, v in report.items()]
        dialog.format_secondary_text("\n".join(msg_lines))
        dialog.run()
        dialog.destroy()


class BuzzardTrayApp:
    """Buzzard Desktop System Tray GTK Application."""

    def __init__(self) -> None:
        if Gtk is None:
            print("GTK3 or PyGObject not available. Control Center requires PyGObject.")
            sys.exit(1)

        icon_str = str(ICON_PATH.resolve()) if ICON_PATH.exists() else "battery-good-symbolic"

        self.indicator = appindicator.Indicator.new(
            "buzzard-tray",
            icon_str,
            appindicator.IndicatorCategory.HARDWARE,
        ) if appindicator else None

        self.window = BuzzardControlWindow(tray_app=self)

        if self.indicator:
            if ICON_PATH.exists():
                self.indicator.set_icon_full(icon_str, "Buzzard Power Suite Logo")
            self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
            self.indicator.set_menu(self.build_menu())

        # Desktop notification on launch
        if Notify:
            try:
                n = Notify.Notification.new("🦅 Buzzard Power Suite", "Control Center & System Tray Active", icon_str)
                n.show()
            except Exception:
                pass

    def build_menu(self) -> any:
        menu = Gtk.Menu()

        status = StatusService.get_status()
        est = PowerEstimator.estimate()
        wattage_str = f"{est['power_draw_w']:.2f} W" if est['power_draw_w'] > 0 else "AC Connected"
        runtime_str = est.get("estimated_runtime", f"{est.get('hours_remaining', 0)}h")

        # Open Window
        win_item = Gtk.MenuItem(label="🦅 Open Buzzard Control Center")
        win_item.connect("activate", lambda w: self.window.show_all())
        menu.append(win_item)
        menu.append(Gtk.SeparatorMenuItem())

        self.header_item = Gtk.MenuItem(label=f"Status: {status['profile'].upper()} ({status['battery_percent']}%)")
        self.header_item.set_sensitive(False)
        menu.append(self.header_item)

        self.telemetry_item = Gtk.MenuItem(label=f"⚡ Draw: {wattage_str} | Runtime: {runtime_str}")
        self.telemetry_item.set_sensitive(False)
        menu.append(self.telemetry_item)

        menu.append(Gtk.SeparatorMenuItem())

        # Profiles Selector Submenu
        profile_menu = Gtk.Menu()
        prof_item = Gtk.MenuItem(label="⚡ Select Power Profile")
        prof_item.set_submenu(profile_menu)

        profiles = [
            ("macmode", "🍏 MacMode (Ultra Saver ~4W)"),
            ("low", "🔋 Low Power Saver"),
            ("hybrid", "⚖️ Hybrid Balanced"),
            ("full", "⚡ Full Performance"),
            ("gaming", "🎮 Gaming Mode"),
            ("creator", "🎨 Creator Mode"),
            ("travel", "✈️ Travel Saver Mode"),
            ("meeting", "🤝 Quiet Meeting Mode"),
            ("auto", "🤖 Auto Mode"),
        ]

        for p_key, p_label in profiles:
            item = Gtk.MenuItem(label=p_label)
            item.connect("activate", self.on_profile_click, p_key)
            profile_menu.append(item)

        menu.append(prof_item)
        menu.append(Gtk.SeparatorMenuItem())

        # Quit
        quit_item = Gtk.MenuItem(label="❌ Quit Buzzard Tray")
        quit_item.connect("activate", Gtk.main_quit)
        menu.append(quit_item)

        menu.show_all()
        return menu

    def refresh_telemetry(self) -> bool:
        """Refreshes tray telemetry menu labels."""
        try:
            status = StatusService.get_status()
            est = PowerEstimator.estimate()
            wattage_str = f"{est['power_draw_w']:.2f} W" if est['power_draw_w'] > 0 else "AC Connected"
            runtime_str = est.get("estimated_runtime", f"{est.get('hours_remaining', 0)}h")

            self.header_item.set_label(f"Status: {status['profile'].upper()} ({status['battery_percent']}%)")
            self.telemetry_item.set_label(f"⚡ Draw: {wattage_str} | Runtime: {runtime_str}")

            if self.indicator:
                self.indicator.set_label(f"{status['battery_percent']}% | {wattage_str}", "buzzard")
        except Exception:
            pass
        return True

    def on_profile_click(self, widget, profile_name: str) -> None:
        ProfileService.apply_profile(profile_name)
        self.window.refresh_telemetry()

    def run(self) -> None:
        if Gtk:
            self.window.show_all()
            Gtk.main()


def main() -> None:
    app = BuzzardTrayApp()
    app.run()


if __name__ == "__main__":
    main()
