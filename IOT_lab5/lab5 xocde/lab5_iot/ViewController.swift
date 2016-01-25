//
//  ViewController.swift
//  lab5_iot
//
//  Created by Yihan Dai, Sihan Wu and Yitong Wang on 15/10/19.
//  All rights reserved.
//

import UIKit
import CoreMotion

class ViewController: UIViewController {
    
    @IBOutlet weak var ipAddress: UITextField! //define a text for the ip address input
    

    @IBOutlet weak var movement: UILabel! //define a label to display the movement of iphone
    
    @IBAction func gripper(sender: UIButton) { //define a button to open or close gripper
        let currentState = sender.currentTitle!
        if currentState == "Open Gripper"{
            self.httpPost("open")     //send "open" and change the state
            sender.setTitle("Close Gripper", forState: UIControlState.Normal)
        }
        else{
            self.httpPost("close") //send "close" and change the state
            sender.setTitle("Open Gripper", forState: UIControlState.Normal)
        
        }
    }
    
    

    
    var Motion = CMMotionManager() //call the function motion manager
    override func viewDidLoad() {
        
        Motion.accelerometerUpdateInterval = 0.2
        Motion.gyroUpdateInterval = 0.2//set the interval
       
        
        Motion.startGyroUpdatesToQueue(NSOperationQueue.currentQueue()!, withHandler: {
            (gyroData: CMGyroData?, error: NSError?) -> Void //call the gyrodata
            in
            self.outputRotationData(gyroData!.rotationRate)
            
            
            if (error != nil){
                print("\(error)")
                
            }
        })
        
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    func outputRotationData(rotation: CMRotationRate){ //set up the different movement for rotation angle
        print("data = \(rotation.x)")
        if rotation.x > 3.0{
            movement?.text = "move up"
            self.httpPost(movement!.text!)
        }
        else if rotation.x < -3.0 {
            movement?.text = "move down"
            self.httpPost(movement!.text!)
        }
        else if rotation.y > 3.0{
            movement?.text = "move forward"
            self.httpPost(movement!.text!)
        }
        else if rotation.y < -3.0{
            movement?.text = "move backward"
            self.httpPost(movement!.text!)
        }
        else if rotation.z > 3.0{
            movement?.text = "move left"
            self.httpPost(movement!.text!)
        }
        else if rotation.z < -3.0{
            movement?.text = "move right"
            self.httpPost(movement!.text!)
        }
    
    }
    
    @IBAction func Reset(sender: AnyObject) { //define a button to reset the state of the robotic arm
        movement?.text = "Static" //show the "static" in the iphone
        self.httpPost("reset") //send the "static" to the raspberri pi
    }
    
  
    
    
   
    
    
    func httpPost(command:String){  //post the message to the raspberri pi
        print("ip is "+ipAddress.text!)
        let request = NSMutableURLRequest(URL: NSURL(string:
            "http://"+ipAddress.text!)!)
        request.HTTPMethod = "POST"
        let postString = command
        request.HTTPBody =    //send the request with the data
            postString.dataUsingEncoding(NSUTF8StringEncoding)
        let task =
        NSURLSession.sharedSession().dataTaskWithRequest(request) {
            data, response, error in
            if error != nil {
                print("error=\(error)")
                return}
            print("response = \(response)")
            let responseString = NSString(data: data!, encoding:
                NSUTF8StringEncoding)
            print("responseString = \(responseString)") //print the response from the server
        }
        task.resume()
    }


}

