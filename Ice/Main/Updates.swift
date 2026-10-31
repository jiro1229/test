// Derived from Ice. Modified for Sora Bar on 2026-10-31.
// Updates stay offline until this fork has its own signed feed.
import SwiftUI

@MainActor
final class UpdatesManager: NSObject, ObservableObject {
    @Published private(set) var canCheckForUpdates = false
    @Published private(set) var lastUpdateCheckDate: Date?

    func performSetup(with appState: AppState) {}

    @objc func checkForUpdates() {
        let alert = NSAlert()
        alert.messageText = "Updates are unavailable in this preview."
        alert.informativeText = "Install a new Sora Bar build manually."
        alert.runModal()
    }
}
