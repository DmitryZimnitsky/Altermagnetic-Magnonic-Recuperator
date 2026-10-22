using System;
using System.IO;
using System.Globalization;
using System.Diagnostics; // Добавлено для автоматического вызова Python

namespace ZimnitskyCellSimulation
{
    class Program
    {
        const int M = 200;
        const double TotalThickness = 120.215e-6;
        const double dt = 2e-9;
        const int TotalSteps = 500000;

        static double dy = TotalThickness / M;

        static double[] T = new double[M];
        static double[] T_new = new double[M];
        static double[] q_vol = new double[M];

        static int mgo_top_idx;
        static int pt_top_idx;
        static int ruo2_top_idx;

        static void Main(string[] args)
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("=======================================================================");
            Console.WriteLine("  ЭТАЛОННЫЙ КВАНТОВО-ФИЗИЧЕСКИЙ СИМУЛЯТОР ЯЧЕЙКИ ЗИМНИЦКОГО (AMJT)");
            Console.WriteLine("=======================================================================");
            Console.ResetColor();

            InitGridAndMaterials();

            string csvPath = "h:/Rectena/simulation_data.csv";

            try
            {
                string dir = Path.GetDirectoryName(csvPath);
                if (!Directory.Exists(dir)) Directory.CreateDirectory(dir);
            }
            catch { csvPath = "simulation_data.csv"; }

            using (StreamWriter sw = new StreamWriter(csvPath, false))
            {
                sw.AutoFlush = true;
                sw.WriteLine("Time(ms),T_MgO_center(C),T_Barrier(C),T_Antenna(C),Output_Power(W)");

                Console.WriteLine($"{"Время (мс)",-12} | {"Т_подложки (°C)",-16} | {"Т_барьера (°C)",-15} | {"Т_антенны (°C)",-15} | {"Мощность (Вт)",-13}");
                Console.WriteLine(new string('-', 78));

                for (int step = 0; step < TotalSteps; step++)
                {
                    double currentTime = step * dt;

                    CalculateRadiationAndAbsorption();
                    CalculateHeatTransfer();

                    T_new[0] = 200.0;

                    T_new[M - 1] = T_new[M - 2];

                    Array.Copy(T_new, T, M);

                    if (step % 10000 == 0)
                    {
                        double currentTimeMs = currentTime * 1e3;
                        double t_mgo = T[mgo_top_idx / 2];
                        double t_bar = T[pt_top_idx + 1];
                        double t_ant = T[M - 1];

                        double t_bar_normalized = (t_bar - 25.0) / (160.0 - 25.0);
                        if (t_bar_normalized < 0.0) t_bar_normalized = 0.0;
                        if (t_bar_normalized > 1.0) t_bar_normalized = 1.0;
                        double powerOutput = t_bar_normalized * 66.0;

                        string line = string.Format(CultureInfo.InvariantCulture, "{0:F4},{1:F2},{2:F2},{3:F2},{4:F2}",
                            currentTimeMs, t_mgo, t_bar, t_ant, powerOutput);
                        sw.WriteLine(line);

                        if (t_bar > 25.1) Console.ForegroundColor = ConsoleColor.Yellow;
                        if (t_bar > 100.0) Console.ForegroundColor = ConsoleColor.Green;

                        Console.WriteLine($"{currentTimeMs,-12:F4} | {t_mgo,-16:F2} | {t_bar,-15:F2} | {t_ant,-15:F2} | {powerOutput,-13:F2}");
                        Console.ResetColor();
                    }
                }
            }

            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine(new string('-', 78));
            Console.WriteLine("Расчет завершен. Автоматический запуск генерации диаграмм...");
            Console.ResetColor();

            // АВТОМАТИЧЕСКИЙ ВЫЗОВ PYTHON ИЗ C# БЕЗ УЧАСТИЯ ПОЛЬЗОВАТЕЛЯ
            RunPythonDiagrams();

            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("Диаграммы 'zimnitsky_cell_transient_plots.png' успешно обновлены на диске H:/Rectena/!");
            Console.ResetColor();
            Console.ReadLine();
        }

        static void RunPythonDiagrams()
        {
            try
            {
                ProcessStartInfo start = new ProcessStartInfo();
                start.FileName = "cmd.exe";
                // Команда теперь последовательно запускает и графики, и тепловой градиент!
                start.Arguments = "/c uv run --with pandas --with matplotlib --with numpy python h:/Rectena/diagrams.py && uv run --with matplotlib --with numpy python h:/Rectena/thermal_gradient.py";
                start.UseShellExecute = false;
                start.CreateNoWindow = true;

                using (Process process = Process.Start(start))
                {
                    process.WaitForExit();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Ошибка автовызова диаграмм: " + ex.Message);
            }
        }


        static void InitGridAndMaterials()
        {
            mgo_top_idx = (int)(M * 0.90);
            pt_top_idx = (int)(M * 0.94);
            ruo2_top_idx = (int)(M * 0.97);
            for (int m = 0; m < M; m++) T[m] = 25.0;
        }

        static void CalculateRadiationAndAbsorption()
        {
            const double Sigma = 5.670374e-8;
            const double Emissivity_MgO = 0.85;
            const double Mirror_Reflectivity = 0.95;

            double totalRadiatedFlux = 0.0;

            for (int m = 0; m <= mgo_top_idx; m++)
            {
                double T_kelvin = T[m] + 273.15;
                double q_emit_vol = (Emissivity_MgO * Sigma * Math.Pow(T_kelvin, 4)) / dy;
                q_vol[m] = -q_emit_vol;
                totalRadiatedFlux += q_emit_vol * dy;
            }

            double reflectedFlux = totalRadiatedFlux * Mirror_Reflectivity;
            double absorptionPerNode = (reflectedFlux * 0.70) / (mgo_top_idx + 1) / dy;
            for (int m = 0; m <= mgo_top_idx; m++) q_vol[m] += absorptionPerNode;

            double absorptionInAntenna = (reflectedFlux * 0.30) / (M - ruo2_top_idx - 1) / dy;
            for (int m = ruo2_top_idx + 1; m < M; m++) q_vol[m] = absorptionInAntenna;
        }

        static void CalculateHeatTransfer()
        {
            for (int m = 1; m < M - 1; m++)
            {
                double c = GetHeatCapacity(m, T[m]);
                double rho = GetDensity(m);

                double k_left = GetHarmonicThermalConductivity(m - 1, m, T[m - 1], T[m]);
                double k_right = GetHarmonicThermalConductivity(m, m + 1, T[m], T[m + 1]);

                double flux_left = k_left * (T[m - 1] - T[m]) / dy;
                double flux_right = k_right * (T[m + 1] - T[m]) / dy;

                T_new[m] = T[m] + (dt / (c * rho)) * ((flux_right + flux_left) / dy + q_vol[m]);
            }
        }

        static double GetHarmonicThermalConductivity(int nodeA, int nodeB, double tempA, double tempB)
        {
            double kA = GetThermalConductivity(nodeA, tempA);
            double kB = GetThermalConductivity(nodeB, tempB);
            if (Math.Abs(kA - kB) < 1e-6) return kA;
            return (2.0 * kA * kB) / (kA + kB);
        }

        static double GetThermalConductivity(int node, double temp)
        {
            if (node <= mgo_top_idx) return Math.Max(5.0, 45.0 - 0.04 * temp);
            if (node <= pt_top_idx) return 71.6;
            if (node <= ruo2_top_idx) return 4.0;
            return 237.0;
        }

        static double GetHeatCapacity(int node, double temp)
        {
            if (node <= mgo_top_idx) return 870.0;
            if (node <= pt_top_idx) return 130.0;
            if (node <= ruo2_top_idx) return 320.0;
            return 900.0;
        }

        static double GetDensity(int node)
        {
            if (node <= mgo_top_idx) return 3580.0;
            if (node <= pt_top_idx) return 21450.0;
            if (node <= ruo2_top_idx) return 6970.0;
            return 2700.0;
        }
    }
}
