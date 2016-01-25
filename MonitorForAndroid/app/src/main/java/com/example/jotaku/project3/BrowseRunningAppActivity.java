package com.example.jotaku.project3;

/**
 * Created by jotaku on 12/3/15.
 */
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import android.app.Activity;
import android.app.ActivityManager;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.pm.PackageManager.NameNotFoundException;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.AdapterView.OnItemClickListener;

public class BrowseRunningAppActivity extends Activity {

    private static String TAG = "BrowseRunningAppActivity";

    private ListView listview = null;

    private List<RunningAppInfo> mlistAppInfo = null;
    private TextView tvInfo = null ;

    private PackageManager pm;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.browse_app_list);

        listview = (ListView) findViewById(R.id.listviewApp);
        tvInfo = (TextView)findViewById(R.id.tvInfo) ;

        mlistAppInfo = new ArrayList<RunningAppInfo>();


        Intent intent = getIntent();

        int pid = intent.getIntExtra("EXTRA_PROCESS_ID", -1);

        if ( pid != -1) {

            mlistAppInfo =querySpecailPIDRunningAppInfo(intent, pid);
        }
        else{

            tvInfo.setText("Android App for E4901");
            mlistAppInfo = queryAllRunningAppInfo();
        }
        BrowseRunningAppAdapter browseAppAdapter = new BrowseRunningAppAdapter(this, mlistAppInfo);
        listview.setAdapter(browseAppAdapter);
    }


    private List<RunningAppInfo> queryAllRunningAppInfo() {
        pm = this.getPackageManager();

        List<ApplicationInfo> listAppcations = pm.getInstalledApplications(PackageManager.GET_UNINSTALLED_PACKAGES);
        Collections.sort(listAppcations,new ApplicationInfo.DisplayNameComparator(pm));


        Map<String, ActivityManager.RunningAppProcessInfo> pgkProcessAppMap = new HashMap<String, ActivityManager.RunningAppProcessInfo>();

        ActivityManager mActivityManager = (ActivityManager) getSystemService(Context.ACTIVITY_SERVICE);

        List<ActivityManager.RunningAppProcessInfo> appProcessList = mActivityManager
                .getRunningAppProcesses();

        for (ActivityManager.RunningAppProcessInfo appProcess : appProcessList) {
            int pid = appProcess.pid;
            String processName = appProcess.processName;
            Log.i(TAG, "processName: " + processName + "  pid: " + pid);

            String[] pkgNameList = appProcess.pkgList;


            for (int i = 0; i < pkgNameList.length; i++) {
                String pkgName = pkgNameList[i];
                Log.i(TAG, "packageName " + pkgName + " at index " + i+ " in process " + pid);

                pgkProcessAppMap.put(pkgName, appProcess);
            }
        }

        List<RunningAppInfo> runningAppInfos = new ArrayList<RunningAppInfo>();

        for (ApplicationInfo app : listAppcations) {

            if (pgkProcessAppMap.containsKey(app.packageName)) {

                int pid = pgkProcessAppMap.get(app.packageName).pid;
                String processName = pgkProcessAppMap.get(app.packageName).processName;
                runningAppInfos.add(getAppInfo(app, pid, processName));
            }
        }

        return runningAppInfos;

    }

    private List<RunningAppInfo> querySpecailPIDRunningAppInfo(Intent intent , int pid) {


        String[] pkgNameList = intent.getStringArrayExtra("EXTRA_PKGNAMELIST");
        String processName = intent.getStringExtra("EXTRA_PROCESS_NAME");


        tvInfo.setText("process id "+pid +", with : "+pkgNameList.length+" process");

        pm = this.getPackageManager();


        List<RunningAppInfo> runningAppInfos = new ArrayList<RunningAppInfo>();

        for(int i = 0 ; i<pkgNameList.length ;i++){

            ApplicationInfo appInfo;
            try {
                appInfo = pm.getApplicationInfo(pkgNameList[i], 0);
                runningAppInfos.add(getAppInfo(appInfo, pid, processName));
            }
            catch (NameNotFoundException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
        return runningAppInfos ;
    }



    private RunningAppInfo getAppInfo(ApplicationInfo app, int pid, String processName) {
        RunningAppInfo appInfo = new RunningAppInfo();
        appInfo.setAppLabel((String) app.loadLabel(pm));
        appInfo.setAppIcon(app.loadIcon(pm));
        appInfo.setPkgName(app.packageName);

        appInfo.setPid(pid);
        appInfo.setProcessName(processName);

        return appInfo;
    }
}
