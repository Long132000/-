namespace Lab14
{
    partial class Form3
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
            this.rbPoint = new System.Windows.Forms.RadioButton();
            this.rbSpline = new System.Windows.Forms.RadioButton();
            this.label1 = new System.Windows.Forms.Label();
            this.numLineWidth = new System.Windows.Forms.NumericUpDown();
            this.btnLineColor = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.btnBgColor = new System.Windows.Forms.Button();
            this.label3 = new System.Windows.Forms.Label();
            this.cbShowLegend = new System.Windows.Forms.CheckBox();
            this.cbShowTitle = new System.Windows.Forms.CheckBox();
            this.groupBox1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numLineWidth)).BeginInit();
            this.SuspendLayout();

            // groupBox1
            this.groupBox1.Controls.Add(this.rbPoint);
            this.groupBox1.Controls.Add(this.rbSpline);
            this.groupBox1.Location = new System.Drawing.Point(12, 12);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(200, 70);
            this.groupBox1.TabIndex = 0;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Тип графика";

            // rbPoint
            this.rbPoint.AutoSize = true;
            this.rbPoint.Location = new System.Drawing.Point(6, 42);
            this.rbPoint.Name = "rbPoint";
            this.rbPoint.Size = new System.Drawing.Size(72, 17);
            this.rbPoint.TabIndex = 1;
            this.rbPoint.Text = "Точечный";
            this.rbPoint.UseVisualStyleBackColor = true;
            this.rbPoint.CheckedChanged += new System.EventHandler(this.SettingChanged);

            // rbSpline
            this.rbSpline.AutoSize = true;
            this.rbSpline.Checked = true;
            this.rbSpline.Location = new System.Drawing.Point(6, 19);
            this.rbSpline.Name = "rbSpline";
            this.rbSpline.Size = new System.Drawing.Size(110, 17);
            this.rbSpline.TabIndex = 0;
            this.rbSpline.TabStop = true;
            this.rbSpline.Text = "Гладкая кривая";
            this.rbSpline.UseVisualStyleBackColor = true;
            this.rbSpline.CheckedChanged += new System.EventHandler(this.SettingChanged);

            // label1
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 95);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(99, 13);
            this.label1.TabIndex = 1;
            this.label1.Text = "Толщина линии:";

            // numLineWidth
            this.numLineWidth.Location = new System.Drawing.Point(117, 93);
            this.numLineWidth.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            0});
            this.numLineWidth.Name = "numLineWidth";
            this.numLineWidth.Size = new System.Drawing.Size(50, 20);
            this.numLineWidth.TabIndex = 2;
            this.numLineWidth.Value = new decimal(new int[] {
            2,
            0,
            0,
            0});
            this.numLineWidth.ValueChanged += new System.EventHandler(this.SettingChanged);

            // btnLineColor
            this.btnLineColor.Location = new System.Drawing.Point(117, 119);
            this.btnLineColor.Name = "btnLineColor";
            this.btnLineColor.Size = new System.Drawing.Size(95, 23);
            this.btnLineColor.TabIndex = 3;
            this.btnLineColor.Text = "Цвет линии";
            this.btnLineColor.UseVisualStyleBackColor = true;
            this.btnLineColor.Click += new System.EventHandler(this.btnLineColor_Click);

            // label2
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 124);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(76, 13);
            this.label2.TabIndex = 4;
            this.label2.Text = "Цвет линии:";

            // btnBgColor
            this.btnBgColor.Location = new System.Drawing.Point(117, 148);
            this.btnBgColor.Name = "btnBgColor";
            this.btnBgColor.Size = new System.Drawing.Size(95, 23);
            this.btnBgColor.TabIndex = 5;
            this.btnBgColor.Text = "Цвет фона";
            this.btnBgColor.UseVisualStyleBackColor = true;
            this.btnBgColor.Click += new System.EventHandler(this.btnBgColor_Click);

            // label3
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(12, 153);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(65, 13);
            this.label3.TabIndex = 6;
            this.label3.Text = "Цвет фона:";

            // cbShowLegend
            this.cbShowLegend.AutoSize = true;
            this.cbShowLegend.Checked = true;
            this.cbShowLegend.CheckState = System.Windows.Forms.CheckState.Checked;
            this.cbShowLegend.Location = new System.Drawing.Point(12, 180);
            this.cbShowLegend.Name = "cbShowLegend";
            this.cbShowLegend.Size = new System.Drawing.Size(117, 17);
            this.cbShowLegend.TabIndex = 7;
            this.cbShowLegend.Text = "Показывать легенду";
            this.cbShowLegend.UseVisualStyleBackColor = true;
            this.cbShowLegend.CheckedChanged += new System.EventHandler(this.SettingChanged);

            // cbShowTitle
            this.cbShowTitle.AutoSize = true;
            this.cbShowTitle.Checked = true;
            this.cbShowTitle.CheckState = System.Windows.Forms.CheckState.Checked;
            this.cbShowTitle.Location = new System.Drawing.Point(12, 203);
            this.cbShowTitle.Name = "cbShowTitle";
            this.cbShowTitle.Size = new System.Drawing.Size(137, 17);
            this.cbShowTitle.TabIndex = 8;
            this.cbShowTitle.Text = "Показывать заголовок";
            this.cbShowTitle.UseVisualStyleBackColor = true;
            this.cbShowTitle.CheckedChanged += new System.EventHandler(this.SettingChanged);

            // Form3
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(224, 231);
            this.Controls.Add(this.cbShowTitle);
            this.Controls.Add(this.cbShowLegend);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.btnBgColor);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.btnLineColor);
            this.Controls.Add(this.numLineWidth);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.groupBox1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow;
            this.Name = "Form3";
            this.Text = "Настройки графика";
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numLineWidth)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        #endregion

        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.RadioButton rbPoint;
        private System.Windows.Forms.RadioButton rbSpline;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.NumericUpDown numLineWidth;
        private System.Windows.Forms.Button btnLineColor;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Button btnBgColor;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.CheckBox cbShowLegend;
        private System.Windows.Forms.CheckBox cbShowTitle;
    }
}