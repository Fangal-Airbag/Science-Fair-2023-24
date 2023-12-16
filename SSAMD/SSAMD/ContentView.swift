//
//  ContentView.swift
//  SSAMD
//
//  Created by Nathaniel's computer on 2023-12-09.
//

import SwiftUI

struct ContentView: View {
    @State private var showAlert = false
    @State private var openCameraView = false
    
    var body: some View {
        NavigationStack {
            ZStack(alignment: .top) {
                RoundedRectangle(cornerRadius:20)
                    .fill(Color.orange)
                    .padding(.bottom)
                    .frame(width: 400, height: 66.0)
                
                VStack(alignment: .center) {
                    Text("SSAMD")
                        .font(.largeTitle)
                        .fontWeight(.semibold)
                        .foregroundColor(Color.black)
                    
                    Text("Shak Sebag, A.I. Melanoma Detector")
                        .font(.subheadline)
                        .foregroundColor(Color.black)
                }
                .padding(.top, 65)
                
                VStack {
                    NavigationLink(destination: CameraView()) {
                        Text("Test yourself!")
                            .font(.largeTitle)
                            .fontWeight(.bold)
                    }
                }
                .padding(.top, 400.0)
                
                HStack {
                    Text("v.SF23H")
                        .foregroundColor(Color.black)
                }
                .padding(.top, 800.0)
                .padding(.trailing, 290.0)
            }
            .edgesIgnoringSafeArea(.top)
            .background(Color.white)
            .edgesIgnoringSafeArea(.bottom)
            
            Spacer()
        }
    }
}

#Preview {
    ContentView()
}
