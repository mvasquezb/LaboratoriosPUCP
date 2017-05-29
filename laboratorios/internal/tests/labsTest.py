from django.test import TestCase
from ..models import *
from ..views import Laboratory


class LaboratoryTestCase(TestCase):
    def setUp(self):
        ## Para probar los tipos de laboratorio
        LaboratoryType.objects.create(typename="Corrosion")
        LaboratoryType.objects.create(typename="Materiales")
        ## laboratorios de prueba
        Laboratory.objects.create(labname="Laboratorio de Corrosion", numUser=30,
                            capacity=50,activate=True,typeLab=1)
        Laboratory.objects.create(labname="Laboratorio de Materiales", numUser=32,
                            capacity=60,activate=True,typeLab=2)

    def test_Laboratory_modify(self):
        lab1= Laboratory.objects.get(pk=1)
        lab2= Laboratory.objects.get(pk=2)
        self.assertEqual(lab1.modify("lab1",60,20,2),"Lab1 con 60 usuarios y 20 "
                                                   "de capacidad y tipo Materiales")
        self.assertEqual(lab2.modify("lab2",60,20,1),"Lab2 con 60 usuarios y 20 "
                                                   "de capacidad y tipo Corrosion")

    def test_Laboratory_delete(self):
        lab1 = Laboratory.objects.get (pk=1)
        self.assertEqual(lab1.deactived(),"Se desactivo")

    def test_Laboratory_create(self):
        countBefore=Laboratory.objects.count()
        Laboratory.create(labname="Laboratorio antisismicos", numUser=30,
                             capacity=50, activate=True,typeLab=1)
        self.assertEqual(Laboratory.objects.count(),countBefore+1)

class TypeLabTest(TestCase):
    def setUp(self):
        LaboratoryType.objects.create(typename="Corrosion", active=True)
        LaboratoryType.objects.create(typename="Materiales", active=True)

    def test_typeLab_modify(self):
        type_lab1 = Laboratory.objects.get(pk=1)
        type_lab2 = Laboratory.objects.get(pk=2)
        self.assertEqual(type_lab1.modify("Tipo3"), "Lab1 es de Tipo3")
        self.assertEqual(type_lab2.modify("Tipo3"), "Lab2 es de Tipo3")

    def test_typelab_delete(self):
        type_lab1 = Laboratory.objects.get(pk=1)
        self.assertEqual(type_lab1.deactived(), "Se desactivo")

    def test_LaboratoryType_create(self):
        countBefore = LaboratoryType.objects.count()
        LaboratoryType.objects.create(typename="Corrosion", active=True)
        self.assertEqual(LaboratoryType.objects.count(), countBefore + 1)

## Pruebas para los tipos de ensayo
class TypeLabAssay(TestCase):
    def setUp(self):
        EssayType.objects.create(typename="TipoEnsayo1", active =True)
        EssayType.objects.create(typename="TipoEnsayo2", active =True)

    def test_typeLab_modify(self):
        type1= EssayType.objects.get(pk=1)
        type2= EssayType.objects.get(pk=2)
        self.assertEqual(type1.modify("TipoEnsayo3"),"Ensayo1 es de TipoEnsayo3")
        self.assertEqual(type2.modify("TipoEnsayo3"),"Ensayo2 es de TipoEnsayo3")

    def test_typelab_delete(self):
        type1 = EssayType.objects.get (pk=1)
        self.assertEqual(type1.deactived(),"Se desactivo")

    def test_LaboratoryType_create(self):
        countBefore=EssayType.objects.count()
        EssayType.objects.create(typename="TipoEnsayo4", active=True)
        self.assertEqual(EssayType.objects.count(),countBefore+1)



class TypeTest(TestCase):
    def setUp(self):
        TypeTest.objects.create(typename="TipoPrueba1", active =True)
        TypeTest.objects.create(typename="TipoPrueba2", active =True)

    def test_typeLab_modify(self):
        type1= TypeTest.objects.get(pk=1)
        type2= TypeTest.objects.get(pk=2)
        self.assertEqual(type1.modify("TipoPrueba3"),"Prueba1 es de TipoPrueba3")
        self.assertEqual(type2.modify("TipoPrueba3"),"Prueba2 es de TipoPrueba3")

    def test_typelab_delete(self):
        type1 = TypeTest.objects.get (pk=1)
        self.assertEqual(type1.deactived(),"Se desactivo")

    def test_LaboratoryType_create(self):
        countBefore=TypeTest.objects.count()
        TypeTest.objects.create(typename="TipoPrueba4", active=True)
        self.assertEqual(TypeTest.objects.count(),countBefore+1)

class TypeSample(TestCase):
    def setUp(self):
        TypeSample.objects.create(typename="TipoMuestra1", active =True)
        TypeSample.objects.create(typename="TipoMuestra2", active =True)

    def test_typeLab_modify(self):
        type1= TypeSample.objects.get(pk=1)
        type2= TypeSample.objects.get(pk=2)
        self.assertEqual(type1.modify("TipoMuestra3"),"Muestra1 es de TipoMuestra3")
        self.assertEqual(type2.modify("TipoMuestra3"),"Muestra2 es de TipoMuestra3")

    def test_typelab_delete(self):
        type1 = TypeSample.objects.get (pk=1)
        self.assertEqual(type1.deactived(),"Se desactivo")

    def test_LaboratoryType_create(self):
        countBefore=TypeSample.objects.count()
        TypeSample.objects.create(typename="TipoMuestra4", active=True)
        self.assertEqual(TypeSample.objects.count(),countBefore+1)

