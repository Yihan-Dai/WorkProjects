package com.example.jotaku.project3;

/**
 * Created by jotaku on 12/3/15.
 */

// to save the system info here
public class ProcessInfo {
    private int pid;
    private int uid;
    private int memSize;
    private String processName;
    private String power;
    private String cpuUsage;


    public String pkgnameList[] ;


    public ProcessInfo(){}

    public int getPid() {
        return pid;
    }

    public void setPid(int pid) {
        this.pid = pid;
    }

    public int getUid() {
        return uid;
    }

    public void setUid(int uid) {
        this.uid = uid;
    }

    public int getMemSize() {
        return memSize;
    }

    public void setMemSize(int memSize) {
        this.memSize = memSize;
    }

    public String getProcessName() {
        return processName;
    }

    public void setPocessName(String processName) {
        this.processName = processName;
    }

    public String getPowerUsage() { return power; }

    public void setPowerUsage(String power) { this.power = power; }

    public String getCpuUsage() { return cpuUsage; }

    public void setCpuUsage(String cpuUsage) { this.cpuUsage = cpuUsage; }
}
