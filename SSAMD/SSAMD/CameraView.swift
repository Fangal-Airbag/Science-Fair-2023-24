//
//  CameraView.swift
//  SSAMD
//
//  Created by Nathaniel's computer on 2023-12-09.
//

import SwiftUI
import PhotosUI

struct CameraView: View {
    @State private var showAlert = false
    @State private var photosPickerItem: PhotosPickerItem?
    @State private var selectedImage: UIImage?
    @State private var predictedLabel: String = ""
    @State private var confidence: Float = 0.0
    
    var body: some View {
        ZStack(alignment: .top) {
            RoundedRectangle(cornerRadius:20)
                .fill(Color.blue)
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
                PhotosPicker(selection: $photosPickerItem, matching: .images) {
                    VStack {
                        Text("Select image")
                            .font(.largeTitle)
                            .fontWeight(.semibold)
                        
                        Group {
                            if let customImage = selectedImage {
                                Image(uiImage: customImage)
                                .resizable()
                                .scaledToFill()
                                .frame(width: 260, height: 260)
                                .clipShape(RoundedRectangle(cornerRadius: 10.0))
                            }
                            else {
                                Image("imageDefault")
                                .resizable()
                                .scaledToFit()
                                .frame(width: 260, height: 260)
                                .clipShape(RoundedRectangle(cornerRadius: 10.0))
                            }
                        }
                    }
                }
                
                VStack(spacing: 25) {
                    Text("Prediction: \(predictedLabel)")
                        .font(.title2)
                        .foregroundColor(Color.black)
                    Text(String(format: "Confidence: %.2f%%", confidence * 100))
                        .font(.title2)
                        .foregroundColor(Color.black)
                }
                .padding(.top, 40.0)
            }
            .padding(.top, 220.0)
            
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
        .onChange(of: photosPickerItem) { _, _ in
            Task {
                if let data = try? await photosPickerItem?.loadTransferable(type: Data.self) {
                    if let selectedImage = UIImage(data: data) {
                        DispatchQueue.main.async {
                            self.selectedImage = selectedImage
                            evaluateImage(selectedImage: selectedImage)
                        }
                    } else {
                        print("Error: Unable to create UIImage from data.")
                    }
                }
            }
        }
        
        Spacer()
    }
    
    func evaluateImage(selectedImage: UIImage) {
        if let resizedImage = selectedImage.resizeTo(targetSize: CGSize(width: 800, height: 800)) {
            guard let imageData = resizedImage.pngData() ?? resizedImage.jpegData(compressionQuality: 1.0) else {
                return
            }

            // Prediction API URL
            let apiUrl = URL(string: "")!

            var request = URLRequest(url: apiUrl)
            request.httpMethod = "POST"
            request.addValue("application/octet-stream", forHTTPHeaderField: "Content-Type")
            request.addValue("", forHTTPHeaderField: "Prediction-key")
            request.httpBody = imageData

            URLSession.shared.dataTask(with: request) { data, response, error in
                guard let data = data, error == nil else {
                    return
                }

                do {
                    let decoder = JSONDecoder()
                    let result = try decoder.decode(PredictionResult.self, from: data)
                    if let prediction = result.predictions.first {
                        DispatchQueue.main.async {
                            self.predictedLabel = prediction.tagName
                            self.confidence = prediction.probability
                        }
                    }
                } catch {
                    print("Error decoding JSON: \(error.localizedDescription)")
                }
            }
            .resume()
        }
    }
}

struct PredictionResult: Decodable {
    let predictions: [Prediction]
}

struct Prediction: Codable {
    let probability: Float
    let tagName: String
}

extension UIImage {
    func resizeTo(targetSize: CGSize) -> UIImage? {
        UIGraphicsBeginImageContext(targetSize)
        defer { UIGraphicsEndImageContext() }
        draw(in: CGRect(origin: .zero, size: targetSize))
        return UIGraphicsGetImageFromCurrentImageContext()
    }
}

#Preview {
    CameraView()
}
