package com.example.jotaku.project3;

/**
 * Created by jotaku on 12/3/15.
 */
import java.io.ByteArrayOutputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.text.DecimalFormat;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.ActivityManager;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.os.Debug;
import android.util.Log;
import android.view.ContextMenu;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ContextMenu.ContextMenuInfo;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.AdapterView.OnItemClickListener;

public class BrowseProcessInfoActivity extends Activity  implements OnItemClickListener{

    private static String TAG = "ProcessInfo";
    private static final int KILL_PORCESS = 1;
    private static final int SEARCH_RUNNING_APP = 2;

    private ActivityManager mActivityManager = null;
    // ProcessInfo Model to save process info
    private List<ProcessInfo> processInfoList = null;

    private ListView listviewProcess;
    private TextView tvTotalProcessNo ;

    private String [] dialogItems  = new String[] {"kill the process","APP running with the process"} ;

    private CpuManager manager;
    private MatrixMultiplication matrix;
    private String powerUsage;
    private String cpuUsage;

    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.browse_process_list);

        listviewProcess = (ListView) findViewById(R.id.listviewProcess);
        listviewProcess.setOnItemClickListener(this);

        tvTotalProcessNo =(TextView)findViewById(R.id.tvTotalProcessNo);


        // set object of ActivityManager
        mActivityManager = (ActivityManager) getSystemService(Context.ACTIVITY_SERVICE);

        manager = new CpuManager(this);
        matrix = new MatrixMultiplication();

//      timeInStateBefor = manager.getTimeInState();

        // get system process info
        getRunningAppProcessInfo();
        // build adapter for listview
        BrowseProcessInfoAdapter mprocessInfoAdapter = new BrowseProcessInfoAdapter(this, processInfoList);
        listviewProcess.setAdapter(mprocessInfoAdapter);

        tvTotalProcessNo.setText("system process number: "+processInfoList.size());
    }
    //kill the process and refresh
    @Override
    public void onItemClick(AdapterView<?> arg0, View arg1,  final int position, long arg3) {
        // TODO Auto-generated method stub
        new AlertDialog.Builder(this).setItems(dialogItems, new DialogInterface.OnClickListener() {

            @SuppressLint("NewApi")
            @Override
            public void onClick(DialogInterface dialog, int which) {
                // TODO Auto-generated method stub
                //kill the process
                if(which == 0) {
                    //release the memory
                    mActivityManager.killBackgroundProcesses(processInfoList.get(position).getProcessName());
                    //refresh the UI
                    getRunningAppProcessInfo() ;
                    BrowseProcessInfoAdapter mprocessInfoAdapter = new BrowseProcessInfoAdapter(
                            BrowseProcessInfoActivity.this, processInfoList);
                    listviewProcess.setAdapter(mprocessInfoAdapter);
                    tvTotalProcessNo.setText("process number:"+processInfoList.size());
                }
                //jump to the APP that running the process
                else if(which ==1){
                    ProcessInfo processInfo = processInfoList.get(position);

                    Intent intent = new Intent() ;
                    intent.putExtra("EXTRA_PKGNAMELIST", processInfo.pkgnameList) ;
                    intent.putExtra("EXTRA_PROCESS_ID", processInfo.getPid());
                    intent.putExtra("EXTRA_PROCESS_NAME", processInfo.getProcessName());
                    intent.setClass(BrowseProcessInfoActivity.this, BrowseRunningAppActivity.class);
                    startActivity(intent);
                }
            }
        }).create().show() ;
    }
    // get system process info
    @SuppressLint("NewApi")
    private void getRunningAppProcessInfo() {
        // Class ProcessInfo Model, to save process info
        processInfoList = new ArrayList<ProcessInfo>();

        // Using getRunningAppProcesses() to access
        List<ActivityManager.RunningAppProcessInfo> appProcessList = mActivityManager
                .getRunningAppProcesses();

        long r_time = 0;
        try {
            r_time = matrix.main(200);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        double totalTime = 0.0;
        for (ActivityManager.RunningAppProcessInfo appProcessInfo : appProcessList) {
            int pid = appProcessInfo.pid;
            double time = getAppProcessTime(pid);
            totalTime = totalTime + time;
        }
        DecimalFormat decimalFormat = new DecimalFormat("0.000");
        DecimalFormat decimalFormat1 = new DecimalFormat("0.0");

        for (ActivityManager.RunningAppProcessInfo appProcessInfo : appProcessList) {
            // process id
            int pid = appProcessInfo.pid;
            // user id
            int uid = appProcessInfo.uid;
            // process battery usage
            double ratio = 100 * getAppProcessTime(pid) / totalTime;
            String num = decimalFormat.format(ratio);
            powerUsage = num;
            //process CPU Usage
            String num1 = decimalFormat1.format(ratio);
            cpuUsage = num1;
            // process name
            String processName = appProcessInfo.processName;
            // process memory size
            int[] myMempid = new int[] { pid };

            Debug.MemoryInfo[] memoryInfo = mActivityManager
                    .getProcessMemoryInfo(myMempid);
            int memSize = memoryInfo[0].dalvikPrivateDirty;
            // for debug
            Log.i(TAG, "processName: " + processName + "  pid: " + pid
                    + " uid:" + uid + " memorySize is -->" + memSize + "kb" + num1);
            // build ProcessInfo Class
            ProcessInfo processInfo = new ProcessInfo();
            processInfo.setPid(pid);
            processInfo.setUid(uid);
            processInfo.setPowerUsage(powerUsage);
            processInfo.setCpuUsage(cpuUsage);
            processInfo.setMemSize(memSize);
            processInfo.setPocessName(processName);
            //save all running process package
            processInfo.pkgnameList = appProcessInfo.pkgList ;
            processInfoList.add(processInfo);

            String[] packageList = appProcessInfo.pkgList;

            Log.i(TAG, "process id is " + pid + "has " + packageList.length);
            for (String pkg : packageList) {
                Log.i(TAG, "packageName " + pkg + " in process id is -->"+ pid);
            }
        }
    }
    // process running time for power usage and cpu usage
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

        if (ret == null) { return 0; }
        String[] s = ret.split(" ");
        if (s == null || s.length < 17) { return 0; }

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
