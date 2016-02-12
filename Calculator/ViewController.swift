//
//  ViewController.swift
//  Calculator
//
//  Created by Yihan Dai on 16/2/11.
//  Copyright © 2016Year Yihan Dai. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    
    @IBOutlet weak var display: UILabel!
    

    @IBOutlet weak var buttonclor: UIButton!

    @IBOutlet weak var buttonclor2: UIButton!

    @IBOutlet weak var buttonclor4: UIButton!
    @IBOutlet weak var buttonclor3: UIButton!
    
    @IBOutlet weak var buttonclor5: UIButton!
    
    @IBOutlet weak var buttonclor6: UIButton!
    
    @IBOutlet weak var buttonclor7: UIButton!
    @IBOutlet weak var buttonclor8: UIButton!
    
    
    
    
    
    @IBOutlet weak var button0: UIButton!
    @IBOutlet weak var buttonclor01: UIButton!
    @IBOutlet weak var buttonclor02: UIButton!
    @IBOutlet weak var button03: UIButton!
    @IBOutlet weak var buttonclor04: UIButton!
    @IBOutlet weak var buttonclor05: UIButton!
    @IBOutlet weak var buttonclor06: UIButton!
    @IBOutlet weak var buttonclor07: UIButton!
    @IBOutlet weak var buttonclor08: UIButton!
    @IBOutlet weak var buttonclor09: UIButton!
    
    
    
    @IBOutlet weak var buttonc: UIButton!
    
    @IBOutlet weak var buttoncomma: UIButton!
    
    
    func dealwithbutton(operation: UIButton){
        operation.backgroundColor = UIColor.brownColor()
        operation.layer.borderColor = UIColor.blackColor().CGColor
        
        operation.layer.borderWidth = 1.0
    }
    
    func dealwithotherbutton(operation: UIButton){
        operation.backgroundColor = UIColor.lightGrayColor()
        operation.layer.borderColor = UIColor.blackColor().CGColor
        
        operation.layer.borderWidth = 1.0
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        display.text = "0"
        view.backgroundColor = UIColor.darkGrayColor()
        dealwithbutton(buttonclor)
        dealwithbutton(buttonclor2)
        dealwithbutton(buttonclor3)
        dealwithbutton(buttonclor4)
        dealwithbutton(buttonclor5)
        
        dealwithotherbutton(buttonclor6)
        dealwithotherbutton(buttonclor7)
        dealwithotherbutton(buttonclor8)
        dealwithotherbutton(buttoncomma)
        dealwithotherbutton(button0)
        dealwithotherbutton(button03)
        dealwithotherbutton(buttonc)
        dealwithotherbutton(buttonclor01)
        dealwithotherbutton(buttonclor02)
        dealwithotherbutton(buttonclor04)
        dealwithotherbutton(buttonclor05)
        dealwithotherbutton(buttonclor06)
        dealwithotherbutton(buttonclor07)
        dealwithotherbutton(buttonclor08)
        dealwithotherbutton(buttonclor09)
        
        display.backgroundColor = UIColor.blackColor()
    }
    var whetheristrue = false
    var operation = "#"
    var digitcurrent = Float32()
    var nextdigit = Float32()
    var doubleinput = false
    var operationisTrue = false
    var secondtime = false
    var operationtime = false
    var whetherneedscolour = true
    func dealwithoperation(operationtype: String){
        switch operation{
        case "+":
            print(Float32(digitcurrent / nextdigit))
            if (digitcurrent + nextdigit)%1 == 0{
                display.text = String(Int(digitcurrent + nextdigit))
            }else{
            display.text = String(digitcurrent + nextdigit)
            }
        case "-" :
            if (digitcurrent - nextdigit)%1 == 0{
                display.text = String(Int(digitcurrent - nextdigit))
            }else{
            display.text = String(digitcurrent-nextdigit)
            }
        case "*":
            if (digitcurrent * nextdigit)%1 == 0{
                display.text = String(Int(digitcurrent * nextdigit))
            }else{
            display.text = String(digitcurrent * nextdigit)
            }
        case "/":
            
            if nextdigit == 0{
                display.text = "Null"
                operationisTrue = false
                whetheristrue = false
                operationisTrue = false
            }
            else{
                if (digitcurrent / nextdigit)%1 == 0 {
                    display.text = String(Int(digitcurrent / nextdigit))
                }else{
                display.text = String(digitcurrent/nextdigit)
                }
            }
        default:()
        }
        operationtime = true
    }
    func dealwithspecialoperator(operationtype: String){
        switch operationtype{
            case "%":
            display.text = String(Float32(display.text!)! / Float32(100))
            case "sqr":
            display.text = String(Float32(display.text!)! * Float32(display.text!)!)
            case "sqrt":
                if Float(display.text!) >= 0{
                    display.text = String(sqrt(Float(display.text!)!))
                }else{
                    display.text = "Null"
                    operationisTrue = false
                    whetheristrue = false
                    operationisTrue = false
            }
        default:()
        }
        whetheristrue = false
    }
    
    @IBAction func operatordigit(sender: UIButton) {
        if whetherneedscolour{
        self.view.backgroundColor = UIColor.greenColor()
        }
        if operationisTrue{
            print(operation)
            if !operationtime{
            dealwithoperation(operation)
            }
            
            switch sender.currentTitle!{
            case "+":
                digitcurrent = Float32(display.text!)!
            case "-":
                digitcurrent = Float32(display.text!)!
            case "*":
                digitcurrent = Float32(display.text!)!
            case "/":
                digitcurrent = Float32(display.text!)!
            case "=":
                operationisTrue = false
                whetheristrue = false
                if whetherneedscolour{
                self.view.backgroundColor = UIColor.grayColor()
                }
            default:()
            }
            doubleinput = false
            operation = sender.currentTitle!
            
        }
        else{
        digitcurrent = Float32(display.text!)!
        if sender.currentTitle! == "%" || sender.currentTitle! == "sqrt" || sender.currentTitle! == "sqr"{
            dealwithspecialoperator(sender.currentTitle!)
            }
        else{
        operation = sender.currentTitle!
        whetheristrue = true
            }
        doubleinput = false
        }
        secondtime = true
    }

    @IBAction func digitappend(sender: UIButton) {
        let digit = sender.currentTitle!
        if whetherneedscolour{
            self.view.backgroundColor = UIColor.blueColor()}
        print(digit)
        operationtime = false
        if whetheristrue{
            if doubleinput{
                display.text = display.text! + digit
                nextdigit = Float32(display.text!)!
            }else{
            if digit == "."{
            display.text = "0"+digit
            }else{
                display.text = digit
                }
            nextdigit = Float32("0"+digit)!
            operationisTrue = true
            doubleinput = true
            }
        }
        else{
            if secondtime{
                if doubleinput{
                    display.text = display.text! + digit
                    if operation == "="{
                        digitcurrent = Float32(display.text!)!
                        
                    }else{
                        nextdigit = Float32(display.text!)!
                    }
                }
                else{
                    if digit == "."{
                        display.text = "0"+digit
                    }else{
                display.text = digit
                    }
                if operation == "="{
                    digitcurrent = Float32(display.text!)!
                    
                }else{
                    nextdigit = Float32(display.text!)!
                    }
                    
                doubleinput = true
                }
            }
        else{
        if display.text! == "0"{
            if digit == "."{
                display.text = display.text! + digit
            }
            else{
                display.text = digit
            }
        }
        else{
            display.text = display.text! + digit
        }
        }
        }
    }
    
    @IBAction func Nobuttonclour(sender: UIButton) {
        let currenttitile = sender.currentTitle!
        if currenttitile == "No Colour"{
            whetherneedscolour = false
            sender.setTitle("Need Colour", forState: UIControlState.Normal)
        }
        else{
            whetherneedscolour = true
            sender.setTitle("No Colour", forState:UIControlState.Normal)
        }
    }
    
    

    
    @IBAction func clear(sender: AnyObject) {
        display.text! = "0"
        secondtime = false
        operationisTrue = false
        whetheristrue = false
        operationtime = false
        if whetherneedscolour{
        self.view.backgroundColor = UIColor.whiteColor()
        }
    }


}

