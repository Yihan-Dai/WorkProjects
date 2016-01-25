package com.example.jotaku.project3;

/**
 * Created by jotaku on 12/5/15.
 */
import android.app.ActivityManager;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.*;
import android.util.Log;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.Process;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class CpuManager {
    private static final String COMMAND_LINE = "/system/bin/cat";
    private static final String PATH_CPU = "/proc/cpuinfo";
    private static final String PATH_MAX = "/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq";
    private static final String PATH_MIN = "/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_min_freq";
    private static final String PATH_CUR = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq";


    private Context mContext;

    private static final String TAG = "BatteryInfo";


    public CpuManager(Context context){
        mContext = context;
    }

    //Get CPU Information
    //Get Max CPU
    public static String getCpuInfo(){
        String result = "";
        ProcessBuilder cmd;
        try{
            String[] args = {COMMAND_LINE, PATH_CPU};
            cmd = new ProcessBuilder(args);
            Process process = cmd.start();
            InputStream in = process.getInputStream();
            byte[] re = new byte[24];
            while (in.read(re) != -1) {
                result = result + new String(re);
            }
            in.close();
        }catch (IOException ex){
            ex.printStackTrace();
            result = "N/A";
        }
        return result.trim();
    }

    //Get Max CPU
    public static String getMaxCpuFreq(){
        String result = "";
        ProcessBuilder cmd;
        try{
            String[] args = {COMMAND_LINE, PATH_MAX};
            cmd = new ProcessBuilder(args);
            Process process = cmd.start();
            InputStream in = process.getInputStream();
            byte[] re = new byte[24];
            int test = in.read(re);
            while (in.read(re) != -1) {
                result = result + new String(re);
            }
            in.close();
        }catch (IOException ex){
            ex.printStackTrace();
            result = "N/A";
        }
        return result.trim();
    }

    //Get Min CPU
    public static String getMinCpuFreq() {
        String result = "";
        ProcessBuilder cmd;
        try {
            String[] args = {COMMAND_LINE, PATH_MIN};
            cmd = new ProcessBuilder(args);
            Process process = cmd.start();
            InputStream in = process.getInputStream();
            byte[] re = new byte[24];
            while (in.read(re) != -1) {
                result = result + new String(re);
            }
            in.close();
        } catch (IOException ex) {
            ex.printStackTrace();
            result = "N/A";
        }
        return result.trim();
    }

    //Get current CPU frequent
    public static String getCurCpuFreq() {
        String result = "N/A";
        try {
            FileReader fr = new FileReader(PATH_CUR);
            BufferedReader br = new BufferedReader(fr);
            String text = br.readLine();
            result = text.trim();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return result;
    }

    //dwy, 11092015
    //main function!!!
    public double measurePowerUsage(String packageNameString) {
        //targetAppTime: CPU Running time of app, totalTime: Total CPU Running time
        HashMap<String, Long> appCpuTimeAfter = new HashMap<String, Long>();
        appCpuTimeAfter = getAppCpuTime(packageNameString);

        double totalPower = 0;
        double targetAppTimeAfter = appCpuTimeAfter.get("targetAppTime");
        //double targetAppTimeBefor = appCpuTimeBefor.get("targetAppTime");
        Log.i(TAG, "appCpuTimeAfter " + targetAppTimeAfter);
        //Log.i(TAG, "appCpuTimeBefor  " + targetAppTimeBefor);

        double totalTimeAfter = appCpuTimeAfter.get("totalTime");
        //double totalTimeBefor = appCpuTimeBefor.get("totalTime");
        Log.i(TAG, "totalTimeAfter " + totalTimeAfter);
        //Log.i(TAG, "totalTimeBefor " + totalTimeBefor);

//        Log.i("AAAAAAAAA", String.valueOf(targetAppTimeAfter-targetAppTimeBefor));
//        Log.i("AAAAAAAAA", String.valueOf(totalTimeAfter-totalTimeBefor));
        double ratio = (targetAppTimeAfter) / (totalTimeAfter);

        Log.i(TAG, "ratio" + ratio);
        double[] currentSteps = getCurrentSteps();

        Log.i(TAG, "currentSteps.length " + currentSteps.length);


        return  ratio; //second to hour
    }

    //get current by frequent, PowerProfile cannot be used, so I use a simple way
    protected double[] getCurrentSteps() {
//        final int speedSteps = mPowerProfile.getNumSpeedSteps(); //amount of CPU working Frequents
        final int speedSteps = 10;
        final double[] powerCpuNormal = new double[speedSteps];
        for (int p = 0; p < speedSteps; p++) {
//            powerCpuNormal[p] = mPowerProfile.getAveragePower(PowerProfile.POWER_CPU_ACTIVE, p);
            powerCpuNormal[p] = 100*(p+1);
        }

        return powerCpuNormal;
    }

    //return CPU time of App
    public HashMap<String, Long> getAppCpuTime(String packageName) {
        HashMap<String, Long> appCpuTime = new HashMap<String, Long>();
        long totalTime = 0;
        long targetProcessTime = 0;

        ActivityManager am = (ActivityManager) mContext.getSystemService(Context.ACTIVITY_SERVICE);
        List<ActivityManager.RunningAppProcessInfo> runningApps = am.getRunningAppProcesses();
        for (ActivityManager.RunningAppProcessInfo info : runningApps) {
            long time = getAppProcessTime(info.pid);
            totalTime += time;
            if (info.processName.contains(packageName)) {
                targetProcessTime += time; //one app may have multiple processes
            }
        }

        appCpuTime.put("totalTime", totalTime);
        appCpuTime.put("targetAppTime", targetProcessTime);

        return appCpuTime;
    }

    //Return CPU running time of some process
    private long getAppProcessTime(int pid) {
        FileInputStream in = null;
        String ret = null;
        try {
            in = new FileInputStream("/proc/" + pid + "/stat");
            byte[] buffer = new byte[1024];
            ByteArrayOutputStream os = new ByteArrayOutputStream();
            int len = 0;
            while ((len = in.read(buffer)) != -1) {
                os.write(buffer, 0, len);
            }
            ret = os.toString();
            os.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (in != null) {
                try {
                    in.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        if (ret == null) {
            return 0;
        }

        String[] s = ret.split(" ");
        if (s == null || s.length < 17) {
            return 0;
        }

        long utime = string2Long(s[13]);
        long stime = string2Long(s[14]);
        long cutime = string2Long(s[15]);
        long cstime = string2Long(s[16]);

        return utime + stime + cutime + cstime;
    }

    private long string2Long(String s) {
        try {
            return Long.parseLong(s);
        } catch (NumberFormatException e) {
        }
        return 0;
    }
}
