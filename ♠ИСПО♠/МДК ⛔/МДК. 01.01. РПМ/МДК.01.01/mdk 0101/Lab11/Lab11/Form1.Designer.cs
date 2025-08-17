namespace Lab11
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
            this.label1 = new System.Windows.Forms.Label();
            this.txtArraySize = new System.Windows.Forms.TextBox();
            this.btnCreateArray = new System.Windows.Forms.Button();
            this.dataGridView1 = new System.Windows.Forms.DataGridView();
            this.btnProcessArray = new System.Windows.Forms.Button();
            this.dataGridView2 = new System.Windows.Forms.DataGridView();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView1)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView2)).BeginInit();
            this.SuspendLayout();

            // label1
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 15);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(121, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "Размер массива (n):";

            // txtArraySize
            this.txtArraySize.Location = new System.Drawing.Point(139, 12);
            this.txtArraySize.Name = "txtArraySize";
            this.txtArraySize.Size = new System.Drawing.Size(100, 20);
            this.txtArraySize.TabIndex = 1;

            // btnCreateArray
            this.btnCreateArray.Location = new System.Drawing.Point(245, 10);
            this.btnCreateArray.Name = "btnCreateArray";
            this.btnCreateArray.Size = new System.Drawing.Size(120, 23);
            this.btnCreateArray.TabIndex = 2;
            this.btnCreateArray.Text = "Создать массив";
            this.btnCreateArray.UseVisualStyleBackColor = true;
            this.btnCreateArray.Click += new System.EventHandler(this.btnCreateArray_Click);

            // dataGridView1
            this.dataGridView1.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridView1.Location = new System.Drawing.Point(12, 60);
            this.dataGridView1.Name = "dataGridView1";
            this.dataGridView1.RowHeadersVisible = false;
            this.dataGridView1.Size = new System.Drawing.Size(353, 80);  // Увеличили высоту с 50 до 80
            this.dataGridView1.TabIndex = 3;

            // btnProcessArray
            this.btnProcessArray.Location = new System.Drawing.Point(12, 116);
            this.btnProcessArray.Name = "btnProcessArray";
            this.btnProcessArray.Size = new System.Drawing.Size(353, 23);
            this.btnProcessArray.TabIndex = 4;
            this.btnProcessArray.Text = "Обработать массив (переставить положительные элементы)";
            this.btnProcessArray.UseVisualStyleBackColor = true;
            this.btnProcessArray.Click += new System.EventHandler(this.btnProcessArray_Click);

            // dataGridView2
            this.dataGridView2.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridView2.Location = new System.Drawing.Point(12, 175);
            this.dataGridView2.Name = "dataGridView2";
            this.dataGridView2.RowHeadersVisible = false;
            this.dataGridView2.Size = new System.Drawing.Size(353, 80);  // Увеличили высоту с 50 до 80
            this.dataGridView2.TabIndex = 5;

            // label2
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 44);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(96, 13);
            this.label2.TabIndex = 6;
            this.label2.Text = "Исходный массив";

            // label3
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(12, 159);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(139, 13);
            this.label3.TabIndex = 7;
            this.label3.Text = "Обработанный массив";

            // Form1
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(377, 267);  // Увеличили высоту формы с 237 до 267
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.dataGridView2);
            this.Controls.Add(this.btnProcessArray);
            this.Controls.Add(this.dataGridView1);
            this.Controls.Add(this.btnCreateArray);
            this.Controls.Add(this.txtArraySize);
            this.Controls.Add(this.label1);
            this.Name = "Form1";
            this.Text = "Обработка массива - вариант 5";
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView1)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView2)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox txtArraySize;
        private System.Windows.Forms.Button btnCreateArray;
        private System.Windows.Forms.DataGridView dataGridView1;
        private System.Windows.Forms.Button btnProcessArray;
        private System.Windows.Forms.DataGridView dataGridView2;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
    }
}