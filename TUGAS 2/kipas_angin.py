import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

suhu = ctrl.Antecedent(np.arange(0, 41, 1), 'suhu')
kelembapan = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembapan')
kecepatan = ctrl.Consequent(np.arange(0, 101, 1), 'kecepatan')

suhu['dingin'] = fuzz.trimf(suhu.universe, [0, 0, 20])
suhu['normal'] = fuzz.trimf(suhu.universe, [15, 25, 35])
suhu['panas'] = fuzz.trimf(suhu.universe, [30, 40, 40])

kelembapan['kering'] = fuzz.trimf(kelembapan.universe, [0, 0, 50])
kelembapan['lembab'] = fuzz.trimf(kelembapan.universe, [30, 50, 70])
kelembapan['basah'] = fuzz.trimf(kelembapan.universe, [50, 100, 100])

kecepatan['lambat'] = fuzz.trimf(kecepatan.universe, [0, 0, 50])
kecepatan['sedang'] = fuzz.trimf(kecepatan.universe, [30, 50, 70])
kecepatan['cepat'] = fuzz.trimf(kecepatan.universe, [60, 100, 100])

rule1 = ctrl.Rule(suhu['dingin'] & kelembapan['kering'], kecepatan['lambat'])
rule2 = ctrl.Rule(suhu['normal'], kecepatan['sedang'])
rule3 = ctrl.Rule(suhu['panas'] | kelembapan['basah'], kecepatan['cepat'])

kipas_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
kipas_simulasi = ctrl.ControlSystemSimulation(kipas_ctrl)

kipas_simulasi.input['suhu'] = 32
kipas_simulasi.input['kelembapan'] = 80

kipas_simulasi.compute()

print(f"Hasil Defuzzifikasi Kecepatan Kipas: {kipas_simulasi.output['kecepatan']:.2f}")

suhu.view()
kelembapan.view()
kecepatan.view(sim=kipas_simulasi)
input("Tekan ENTER untuk menutup grafik...")