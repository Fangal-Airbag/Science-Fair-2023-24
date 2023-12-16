//
//  SSAMDApp.swift
//  SSAMD
//
//  Created by Nathaniel's computer on 2023-12-09.
//

import SwiftUI

@main
struct SSAMDApp: App {
    @State private var showAlert = false

    var body: some Scene {
        WindowGroup {
            ContentView()
                .alert(isPresented: $showAlert) {
                    Alert(
                        title: Text("Notice"),
                        message: Text("We are pleased to welcome you to the SSAMD app! Our app utilizes an AI prediction model, trained on over 10,000 images, to diagnose suspicious lesions as benign or malignant.\n\nIn order to get the most accurate results, please make sure to utilize a clear image that is cropped to focus on the area of suspicion.\n\nIt is extremely important that if you have any concerns, regardless of the AI's prediction, that you should seek out an immediate proffesional consultation."),
                        dismissButton: .default(Text("Continue"))
                    )
                }
                .onAppear {
                    showAlert = true
                }
        }
    }
}
