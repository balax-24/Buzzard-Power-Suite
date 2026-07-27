"""Buzzard System Tray GUI Application & Real-Time Battery Telemetry Engine.

Provides a GTK3/AppIndicator desktop tray icon with live battery power draw (W),
time remaining, dynamic profile switching, and hardware controls (80% charge limit, refresh rate, Turbo boost).
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
    try:
        gi.require_version("AppIndicator3", "0.1")
        from gi.repository import AppIndicator3 as appindicator
    except Exception:
        try:
            gi.require_version("AyatanaAppIndicator3", "0.1")
            from gi.repository import AyatanaAppIndicator3 as appindicator
        except Exception:
            appindicator = None
    from gi.repository import GLib, Gtk
except ImportError:
    Gtk = None
    appindicator = None

ICON_PATH = Path(__file__).parent.parent / "assets" / "buzzard.png"


class BuzzardTrayApp:
    """Buzzard Desktop System Tray GTK Application."""

    def __init__(self) -> None:
        if Gtk is None:
            print("GTK3 or PyGObject not available. System tray application requires PyGObject.")
            sys.exit(1)

        icon_str = str(ICON_PATH.resolve()) if ICON_PATH.exists() else "battery-good-symbolic"

        self.indicator = appindicator.Indicator.new(
            "buzzard-tray",
            icon_str,
            appindicator.IndicatorCategory.HARDWARE,
        ) if appindicator else None

        if self.indicator:
            if ICON_PATH.exists():
                self.indicator.set_icon_full(icon_str, "Buzzard Power Suite Logo")
            self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
            self.indicator.set_menu(self.build_menu())
            # Periodically refresh tray status and telemetry every 3 seconds
            GLib.timeout_add_seconds(3, self.refresh_telemetry)

    def build_menu(self) -> any:
        menu = Gtk.Menu()

        # 1. Header & Live Telemetry Item
        status = StatusService.get_status()
        est = PowerEstimator.estimate()
        wattage_str = f"{est['power_draw_w']:.2f} W" if est['power_draw_w'] > 0 else "AC Connected"
        
        self.header_item = Gtk.MenuItem(label=f"🦅 Buzzard: {status['profile'].upper()} ({status['battery_percent']}%)")
        self.header_item.set_sensitive(False)
        menu.append(self.header_item)

        self.telemetry_item = Gtk.MenuItem(label=f"⚡ Draw: {wattage_str} | Runtime: {est['time_remaining_hours']}h")
        self.telemetry_item.set_sensitive(False)
        menu.append(self.telemetry_item)

        menu.append(Gtk.SeparatorMenuItem())

        # 2. Profiles Selector Submenu
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

        # 3. Quick Hardware Controls Submenu
        ctrl_menu = Gtk.Menu()
        ctrl_item = Gtk.MenuItem(label="⚙️ Hardware Controls")
        ctrl_item.set_submenu(ctrl_menu)

        # Battery Charge Limit 80%
        chg_80 = Gtk.MenuItem(label="🔋 Limit Charge to 80% (Conservation)")
        chg_80.connect("activate", lambda w: VendorManager.apply_vendor_settings({"battery_charge_limit": 80}))
        ctrl_menu.append(chg_80)

        # Battery Charge Limit 100%
        chg_100 = Gtk.MenuItem(label="🔋 Limit Charge to 100% (Full)")
        chg_100.connect("activate", lambda w: VendorManager.apply_vendor_settings({"battery_charge_limit": 100}))
        ctrl_menu.append(chg_100)

        ctrl_menu.append(Gtk.SeparatorMenuItem())

        # Display Refresh Rates
        rr_60 = Gtk.MenuItem(label="🖥️ Set Refresh Rate: 60Hz")
        rr_60.connect("activate", lambda w: DisplayManager.set_refresh_rate(60))
        ctrl_menu.append(rr_60)

        rr_120 = Gtk.MenuItem(label="🖥️ Set Refresh Rate: 120Hz")
        rr_120.connect("activate", lambda w: DisplayManager.set_refresh_rate(120))
        ctrl_menu.append(rr_120)

        rr_144 = Gtk.MenuItem(label="🖥️ Set Refresh Rate: 144Hz")
        rr_144.connect("activate", lambda w: DisplayManager.set_refresh_rate(144))
        ctrl_menu.append(rr_144)

        menu.append(ctrl_item)
        menu.append(Gtk.SeparatorMenuItem())

        # 4. System Diagnostics
        doc_item = Gtk.MenuItem(label="🩺 Run System Doctor Diagnostics")
        doc_item.connect("activate", self.on_doctor_click)
        menu.append(doc_item)

        # 5. Quit
        quit_item = Gtk.MenuItem(label="❌ Quit Buzzard Tray")
        quit_item.connect("activate", Gtk.main_quit)
        menu.append(quit_item)

        menu.show_all()
        return menu

    def refresh_telemetry(self) -> bool:
        """Periodically refreshes tray telemetry and menu label."""
        try:
            status = StatusService.get_status()
            est = PowerEstimator.estimate()
            wattage_str = f"{est['power_draw_w']:.2f} W" if est['power_draw_w'] > 0 else "AC Connected"

            self.header_item.set_label(f"🦅 Buzzard: {status['profile'].upper()} ({status['battery_percent']}%)")
            self.telemetry_item.set_label(f"⚡ Draw: {wattage_str} | Runtime: {est['time_remaining_hours']}h")

            if self.indicator:
                self.indicator.set_label(f"{status['battery_percent']}% | {wattage_str}", "buzzard")
        except Exception:
            pass
        return True  # Keep GLib timer active

    def on_profile_click(self, widget, profile_name: str) -> None:
        ProfileService.apply_profile(profile_name)
        self.refresh_telemetry()

    def on_doctor_click(self, widget) -> None:
        report = DiagnosticService.report()
        print("Buzzard System Doctor Diagnostics:", report)

    def run(self) -> None:
        if Gtk:
            Gtk.main()


def main() -> None:
    app = BuzzardTrayApp()
    app.run()


if __name__ == "__main__":
    main()
