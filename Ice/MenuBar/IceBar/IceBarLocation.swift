// Modified for Sora Bar on 2026-10-31. Original Ice attribution retained.
//
//  IceBarLocation.swift
//  Ice
//

import SwiftUI

/// Locations where the Sora Panel can appear.
enum IceBarLocation: Int, CaseIterable, Identifiable {
    /// The Sora Panel will appear in different locations based on context.
    case dynamic = 0

    /// The Sora Panel will appear centered below the mouse pointer.
    case mousePointer = 1

    /// The Sora Panel will appear centered below the Sora Bar icon.
    case iceIcon = 2

    var id: Int { rawValue }

    /// Localized string key representation.
    var localized: LocalizedStringKey {
        switch self {
        case .dynamic: "Dynamic"
        case .mousePointer: "Mouse pointer"
        case .iceIcon: "Sora Bar icon"
        }
    }
}
