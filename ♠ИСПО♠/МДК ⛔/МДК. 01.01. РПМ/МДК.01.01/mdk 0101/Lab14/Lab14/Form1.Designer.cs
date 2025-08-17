namespace Lab14
{
    partial class Form1
    {
        private System.ComponentModel.IContainer components = null;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        private void InitializeComponent()
        {
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.rbFunc3 = new System.Windows.Forms.RadioButton();
            this.rbFunc2 = new System.Windows.Forms.RadioButton();
            this.rbFunc1 = new System.Windows.Forms.RadioButton();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.rbPoints = new System.Windows.Forms.RadioButton();
            this.rbStep = new System.Windows.Forms.RadioButton();
            this.label1 = new System.Windows.Forms.Label();
            this.txtXStart = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.txtXEnd = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.txtStep = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.txtCoeff = new System.Windows.Forms.TextBox();
            this.btnCompute = new System.Windows.Forms.Button();
            this.txtPoints = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.groupBox1.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.SuspendLayout();
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.rbFunc3);
            this.groupBox1.Controls.Add(this.rbFunc2);
            this.groupBox1.Controls.Add(this.rbFunc1);
            this.groupBox1.Location = new System.Drawing.Point(12, 12);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(200, 100);
            this.groupBox1.TabIndex = 0;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Выберите функцию";
            // 
            // rbFunc3
            // 
            this.rbFunc3.AutoSize = true;
            this.rbFunc3.Location = new System.Drawing.Point(6, 65);
            this.rbFunc3.Name = "rbFunc3";
            this.rbFunc3.Size = new System.Drawing.Size(68, 17);
            this.rbFunc3.TabIndex = 2;
            this.rbFunc3.Text = "-a * e^x";
            this.rbFunc3.UseVisualStyleBackColor = true;
            this.rbFunc3.CheckedChanged += new System.EventHandler(this.ValidateInputs);
            // 
            // rbFunc2
            // 
            this.rbFunc2.AutoSize = true;
            this.rbFunc2.Location = new System.Drawing.Point(6, 42);
            this.rbFunc2.Name = "rbFunc2";
            this.rbFunc2.Size = new System.Drawing.Size(84, 17);
            this.rbFunc2.TabIndex = 1;
            this.rbFunc2.Text = "a * e^(2x)";
            this.rbFunc2.UseVisualStyleBackColor = true;
            this.rbFunc2.CheckedChanged += new System.EventHandler(this.ValidateInputs);
            // 
            // rbFunc1
            // 
            this.rbFunc1.AutoSize = true;
            this.rbFunc1.Location = new System.Drawing.Point(6, 19);
            this.rbFunc1.Name = "rbFunc1";
            this.rbFunc1.Size = new System.Drawing.Size(61, 17);
            this.rbFunc1.TabIndex = 0;
            this.rbFunc1.Text = "a * e^x";
            this.rbFunc1.UseVisualStyleBackColor = true;
            this.rbFunc1.CheckedChanged += new System.EventHandler(this.ValidateInputs);
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.txtPoints);
            this.groupBox2.Controls.Add(this.label5);
            this.groupBox2.Controls.Add(this.rbPoints);
            this.groupBox2.Controls.Add(this.rbStep);
            this.groupBox2.Location = new System.Drawing.Point(218, 12);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(200, 100);
            this.groupBox2.TabIndex = 1;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "Метод расчета";
            // 
            // rbPoints
            // 
            this.rbPoints.AutoSize = true;
            this.rbPoints.Location = new System.Drawing.Point(6, 42);
            this.rbPoints.Name = "rbPoints";
            this.rbPoints.Size = new System.Drawing.Size(108, 17);
            this.rbPoints.TabIndex = 1;
            this.rbPoints.Text = "Количество точек";
            this.rbPoints.UseVisualStyleBackColor = true;
            this.rbPoints.CheckedChanged += new System.EventHandler(this.rbStep_CheckedChanged);
            // 
            // rbStep
            // 
            this.rbStep.AutoSize = true;
            this.rbStep.Checked = true;
            this.rbStep.Location = new System.Drawing.Point(6, 19);
            this.rbStep.Name = "rbStep";
            this.rbStep.Size = new System.Drawing.Size(48, 17);
            this.rbStep.TabIndex = 0;
            this.rbStep.TabStop = true;
            this.rbStep.Text = "Шаг";
            this.rbStep.UseVisualStyleBackColor = true;
            this.rbStep.CheckedChanged += new System.EventHandler(this.rbStep_CheckedChanged);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 125);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(74, 13);
            this.label1.TabIndex = 2;
            this.label1.Text = "Начало (Xнач)";
            // 
            // txtXStart
            // 
            this.txtXStart.Location = new System.Drawing.Point(12, 141);
            this.txtXStart.Name = "txtXStart";
            this.txtXStart.Size = new System.Drawing.Size(100, 20);
            this.txtXStart.TabIndex = 3;
            this.txtXStart.TextChanged += new System.EventHandler(this.ValidateInputs);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(118, 125);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(68, 13);
            this.label2.TabIndex = 4;
            this.label2.Text = "Конец (Xкон)";
            // 
            // txtXEnd
            // 
            this.txtXEnd.Location = new System.Drawing.Point(118, 141);
            this.txtXEnd.Name = "txtXEnd";
            this.txtXEnd.Size = new System.Drawing.Size(100, 20);
            this.txtXEnd.TabIndex = 5;
            this.txtXEnd.TextChanged += new System.EventHandler(this.ValidateInputs);
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(224, 125);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(45, 13);
            this.label3.TabIndex = 6;
            this.label3.Text = "Шаг (dX)";
            // 
            // txtStep
            // 
            this.txtStep.Location = new System.Drawing.Point(224, 141);
            this.txtStep.Name = "txtStep";
            this.txtStep.Size = new System.Drawing.Size(100, 20);
            this.txtStep.TabIndex = 7;
            this.txtStep.TextChanged += new System.EventHandler(this.ValidateInputs);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(12, 164);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(67, 13);
            this.label4.TabIndex = 8;
            this.label4.Text = "Коэффициент (a)";
            // 
            // txtCoeff
            // 
            this.txtCoeff.Location = new System.Drawing.Point(12, 180);
            this.txtCoeff.Name = "txtCoeff";
            this.txtCoeff.Size = new System.Drawing.Size(100, 20);
            this.txtCoeff.TabIndex = 9;
            this.txtCoeff.TextChanged += new System.EventHandler(this.ValidateInputs);
            // 
            // btnCompute
            // 
            this.btnCompute.Enabled = false;
            this.btnCompute.Location = new System.Drawing.Point(118, 178);
            this.btnCompute.Name = "btnCompute";
            this.btnCompute.Size = new System.Drawing.Size(206, 23);
            this.btnCompute.TabIndex = 10;
            this.btnCompute.Text = "Построить график";
            this.btnCompute.UseVisualStyleBackColor = true;
            this.btnCompute.Click += new System.EventHandler(this.btnCompute_Click);
            // 
            // txtPoints
            // 
            this.txtPoints.Enabled = false;
            this.txtPoints.Location = new System.Drawing.Point(120, 65);
            this.txtPoints.Name = "txtPoints";
            this.txtPoints.Size = new System.Drawing.Size(74, 20);
            this.txtPoints.TabIndex = 3;
            this.txtPoints.TextChanged += new System.EventHandler(this.ValidateInputs);
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(120, 49);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(66, 13);
            this.label5.TabIndex = 2;
            this.label5.Text = "Количество:";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(434, 211);
            this.Controls.Add(this.btnCompute);
            this.Controls.Add(this.txtCoeff);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.txtStep);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.txtXEnd);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.txtXStart);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.groupBox1);
            this.Name = "Form1";
            this.Text = "Построение графиков (Вариант 6)";
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.RadioButton rbFunc3;
        private System.Windows.Forms.RadioButton rbFunc2;
        private System.Windows.Forms.RadioButton rbFunc1;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.RadioButton rbPoints;
        private System.Windows.Forms.RadioButton rbStep;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox txtXStart;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox txtXEnd;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox txtStep;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox txtCoeff;
        private System.Windows.Forms.Button btnCompute;
        private System.Windows.Forms.TextBox txtPoints;
        private System.Windows.Forms.Label label5;
    }
}