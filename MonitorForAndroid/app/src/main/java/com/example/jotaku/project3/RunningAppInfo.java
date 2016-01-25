package com.example.jotaku.project3;

/**
 * Created by jotaku on 12/3/15.
 */

import android.content.Intent;
import android.graphics.drawable.Drawable;

// to save running app info here
public class RunningAppInfo {
    private String appLabel;
    private Drawable appIcon ;
    private String pkgName ;

    private int pid ;
    private String processName ;

    public RunningAppInfo(){}

    public String getAppLabel() {
        return appLabel;
    }
    public void setAppLabel(String appName) {
        this.appLabel = appName;
    }
    public Drawable getAppIcon() {
        return appIcon;
    }
    public void setAppIcon(Drawable appIcon) {
        this.appIcon = appIcon;
    }
    public String getPkgName(){
        return pkgName ;
    }
    public void setPkgName(String pkgName){
        this.pkgName=pkgName ;
    }

    public int getPid() {
        return pid;
    }

    public void setPid(int pid) {
        this.pid = pid;
    }

    public String getProcessName() {
        return processName;
    }

    public void setProcessName(String processName) {
        this.processName = processName;
    }

}
