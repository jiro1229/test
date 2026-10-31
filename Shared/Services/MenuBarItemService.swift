// Modified for Sora Bar on 2026-10-31. Original Ice attribution retained.
//
//  MenuBarItemService.swift
//  Shared
//

import Foundation

enum MenuBarItemService {
    static let name = "local.sorabar.app.MenuBarItemService"
}

extension MenuBarItemService {
    enum Request: Codable {
        case start
        case sourcePID(WindowInfo)
    }

    enum Response: Codable {
        case start
        case sourcePID(pid_t?)
    }
}
