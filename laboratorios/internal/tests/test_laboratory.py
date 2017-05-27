from django.test import TestCase
from internal.models import *


class LabsTestCase(TestCase):
    def setUp(self):
        # Para probar los tipos de laboratorio
        LaboratoryType.objects.create(name="Corrosion")
        LaboratoryType.objects.create(name="Materiales")
        # laboratorios de prueba
        Laboratory.objects.create(name="Laboratorio de Corrosion", users_number=30,
                            capacity=50, active=True, type=1)
        Laboratory.objects.create(name="Laboratorio de Materiales", users_number=32,
                            capacity=60, active=True, type=2)

    def test_labs_modify(self):
        lab1 = Laboratory.objects.get(pk=1)
        lab2 = Laboratory.objects.get(pk=2)
        self.assertEqual(lab1.modify("lab1", 60, 20, 2), "Lab1 con 60 usuarios y 20 "
                         "de capacidad y tipo Materiales")
        self.assertEqual(lab2.modify("lab2", 60, 20, 1), "Lab2 con 60 usuarios y 20 "
                         "de capacidad y tipo Corrosion")

    def test_labs_delete(self):
        lab1 = Laboratory.objects.get(pk=1)
        self.assertEqual(lab1.deactived(), "Se desactivo")

    def test_labs_create(self):
        countBefore = Laboratory.objects.count()
        Laboratory.objects.create(name="Laboratorio antisismicos", users_number=30,
                            capacity=50, active=True, type=1)
        self.assertEqual(Laboratory.objects.count(), countBefore + 1)


class TypeLabCase(TestCase):
    def setUp(self):
        LaboratoryType.objects.create(name="Corrosion", active=True)
        LaboratoryType.objects.create(name="Materiales", active=True)

    def test_typeLab_modify(self):
        type_lab1 = Laboratory.objects.get(pk=1)
        type_lab2 = Laboratory.objects.get(pk=2)
        self.assertEqual(type_lab1.modify("Tipo3"), "Lab1 es de Tipo3")
        self.assertEqual(type_lab2.modify("Tipo3"), "Lab2 es de Tipo3")

    def test_typelab_delete(self):
        type_lab1 = Laboratory.objects.get(pk=1)
        self.assertEqual(type_lab1.active, False)

    def test_typelabs_create(self):
        countBefore = LaboratoryType.objects.count()
        LaboratoryType.objects.create(name="Corrosion", active=True)
        self.assertEqual(LaboratoryType.objects.count(), countBefore + 1)

# Pruebas para los tipos de ensayo


class EssayTypeCase(TestCase):
    def setUp(self):
        EssayType.objects.create(name="TipoEnsayo1", active=True)
        EssayType.objects.create(name="TipoEnsayo2", active=True)

    def test_typeLab_modify(self):
        type1 = EssayType.objects.get(pk=1)
        type2 = EssayType.objects.get(pk=2)
        self.assertEqual(type1.modify("TipoEnsayo3"),
                         "Ensayo1 es de TipoEnsayo3")
        self.assertEqual(type2.modify("TipoEnsayo3"),
                         "Ensayo2 es de TipoEnsayo3")

    def test_typelab_delete(self):
        type1 = EssayType.objects.get(pk=1)
        self.assertEqual(type1.active, False)

    def test_typelabs_create(self):
        countBefore = EssayType.objects.count()
        EssayType.objects.create(name="TipoEnsayo4", active=True)
        self.assertEqual(EssayType.objects.count(), countBefore + 1)


class TestTypeCase(TestCase):
    def setUp(self):
        TestType.objects.create(name="TipoPrueba1", active=True)
        TestType.objects.create(name="TipoPrueba2", active=True)

    def test_typeLab_modify(self):
        type1 = TestType.objects.get(pk=1)
        type2 = TestType.objects.get(pk=2)
        self.assertEqual(type1.modify("TipoPrueba3"),
                         "Prueba1 es de TipoPrueba3")
        self.assertEqual(type2.modify("TipoPrueba3"),
                         "Prueba2 es de TipoPrueba3")

    def test_typelab_delete(self):
        type1 = TestType.objects.get(pk=1)
        self.assertEqual(type1.deactived(), "Se desactivo")

    def test_typelabs_create(self):
        countBefore = TestType.objects.count()
        TestType.objects.create(name="TipoPrueba4", active=True)
        self.assertEqual(TestType.objects.count(), countBefore + 1)


class SampleTypeCase(TestCase):
    def setUp(self):
        SampleType.objects.create(name="TipoMuestra1", active=True)
        SampleType.objects.create(name="TipoMuestra2", active=True)

    def test_typeLab_modify(self):
        type1 = SampleType.objects.get(pk=1)
        type2 = SampleType.objects.get(pk=2)
        self.assertEqual(type1.modify("TipoMuestra3"),
                         "Muestra1 es de TipoMuestra3")
        self.assertEqual(type2.modify("TipoMuestra3"),
                         "Muestra2 es de TipoMuestra3")

    def test_typelab_delete(self):
        type1 = SampleType.objects.get(pk=1)
        self.assertEqual(type1.active, False)

    def test_typelabs_create(self):
        countBefore = SampleType.objects.count()
        SampleType.objects.create(name="TipoMuestra4", active=True)
        self.assertEqual(SampleType.objects.count(), countBefore + 1)
