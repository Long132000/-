namespace Lab13
{
    partial class Form2
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

        private void InitializeComponent()
        {
            this.label1 = new System.Windows.Forms.Label();
            this.linkLabelForward = new System.Windows.Forms.LinkLabel();
            this.linkLabelBackward = new System.Windows.Forms.LinkLabel();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.trackBarSpeed = new System.Windows.Forms.TrackBar();
            this.label4 = new System.Windows.Forms.Label();
            this.comboBoxShape = new System.Windows.Forms.ComboBox();
            this.label5 = new System.Windows.Forms.Label();
            this.comboBoxDirection = new System.Windows.Forms.ComboBox();
            ((System.ComponentModel.ISupportInitialize)(this.trackBarSpeed)).BeginInit();
            this.SuspendLayout();

            // label1 (Цвет вперед)
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 20);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(112, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "Цвет растягивания:";

            // linkLabelForward (Выбор цвета)
            this.linkLabelForward.AutoSize = true;
            this.linkLabelForward.Location = new System.Drawing.Point(130, 20);
            this.linkLabelForward.Name = "linkLabelForward";
            this.linkLabelForward.Size = new System.Drawing.Size(84, 13);
            this.linkLabelForward.TabIndex = 1;
            this.linkLabelForward.TabStop = true;
            this.linkLabelForward.Text = "Выбрать цвет";
            this.linkLabelForward.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.linkLabelForward_LinkClicked);

            // linkLabelBackward (Выбор цвета)
            this.linkLabelBackward.AutoSize = true;
            this.linkLabelBackward.Location = new System.Drawing.Point(130, 50);
            this.linkLabelBackward.Name = "linkLabelBackward";
            this.linkLabelBackward.Size = new System.Drawing.Size(84, 13);
            this.linkLabelBackward.TabIndex = 3;
            this.linkLabelBackward.TabStop = true;
            this.linkLabelBackward.Text = "Выбрать цвет";
            this.linkLabelBackward.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.linkLabelBackward_LinkClicked);

            // label2 (Цвет назад)
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 50);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(106, 13);
            this.label2.TabIndex = 2;
            this.label2.Text = "Цвет сжатия:";

            // label3 (Скорость)
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(12, 80);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(58, 13);
            this.label3.TabIndex = 4;
            this.label3.Text = "Скорость:";

            // trackBarSpeed
            this.trackBarSpeed.Location = new System.Drawing.Point(15, 100);
            this.trackBarSpeed.Maximum = 100;
            this.trackBarSpeed.Minimum = 1;
            this.trackBarSpeed.Value = 50;
            this.trackBarSpeed.Name = "trackBarSpeed";
            this.trackBarSpeed.Size = new System.Drawing.Size(200, 45);
            this.trackBarSpeed.TabIndex = 5;
            this.trackBarSpeed.Scroll += new System.EventHandler(this.trackBarSpeed_Scroll);

            // label4 (Форма)
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(12, 140);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(47, 13);
            this.label4.TabIndex = 6;
            this.label4.Text = "Форма:";

            // comboBoxShape
            this.comboBoxShape.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxShape.FormattingEnabled = true;
            this.comboBoxShape.Items.AddRange(new object[] {
                "Круг",
                "Квадрат",
                "Ромб"});
            this.comboBoxShape.Location = new System.Drawing.Point(65, 137);
            this.comboBoxShape.Name = "comboBoxShape";
            this.comboBoxShape.Size = new System.Drawing.Size(120, 21);
            this.comboBoxShape.TabIndex = 7;
            this.comboBoxShape.SelectedIndexChanged += new System.EventHandler(this.comboBoxShape_SelectedIndexChanged);

            // label5 (Направление)
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(12, 170);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(76, 13);
            this.label5.TabIndex = 8;
            this.label5.Text = "Направление:";

            // comboBoxDirection
            this.comboBoxDirection.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxDirection.FormattingEnabled = true;
            this.comboBoxDirection.Items.AddRange(new object[] {
                "Вверх-Вниз",
                "Влево-Вправо"});
            this.comboBoxDirection.Location = new System.Drawing.Point(95, 167);
            this.comboBoxDirection.Name = "comboBoxDirection";
            this.comboBoxDirection.Size = new System.Drawing.Size(120, 21);
            this.comboBoxDirection.TabIndex = 9;
            this.comboBoxDirection.SelectedIndexChanged += new System.EventHandler(this.comboBoxDirection_SelectedIndexChanged);

            // Form2
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(230, 210);
            this.Controls.Add(this.comboBoxDirection);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.comboBoxShape);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.trackBarSpeed);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.linkLabelBackward);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.linkLabelForward);
            this.Controls.Add(this.label1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "Form2";
            this.Text = "Настройки";
            ((System.ComponentModel.ISupportInitialize)(this.trackBarSpeed)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.LinkLabel linkLabelForward;
        private System.Windows.Forms.LinkLabel linkLabelBackward;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TrackBar trackBarSpeed;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.ComboBox comboBoxShape;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.ComboBox comboBoxDirection;
    }
}