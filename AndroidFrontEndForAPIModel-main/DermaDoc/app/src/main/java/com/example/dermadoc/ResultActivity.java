package com.example.dermadoc;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.TextView;

public class ResultActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result);
        this.setValues();
    }

    public void setValues(){
        Bundle bundle = getIntent().getExtras();
        String result = bundle.getString("result");
        TextView headerView = findViewById(R.id.resultHeaderTextView);
        TextView responseView = findViewById(R.id.resultTextView);
        if(result.equalsIgnoreCase("Melanoma")){
            headerView.setText("You have");
            responseView.setText("Melanoma");
        }else if (result.equalsIgnoreCase("Not Melanoma")){
            headerView.setText("You do not have");
            responseView.setText("Melanoma");
        }
    }
}