from django.test import TestCase
from ..models import *

class LabsTestCase(TestCase):
    def setUp(self):
        ## Para probar los tipos de laboratorio
        TypeLabs.objects.create(typename="Corrosion")
        TypeLabs.objects.create(typename="Materiales")
        ## laboratorios de prueba
        Labs.objects.create(labname="Laboratorio de Corrosion", numUser=30,
                            capacity=50,activate=True,typeLab=1)
        Labs.objects.create(labname="Laboratorio de Materiales", numUser=32,
                            capacity=60,activate=True,typeLab=2)

    def test_labs_modify(self):
        lab1= Labs.objects.get(pk=1)
        lab2= Labs.objects.get(pk=2)
        self.assertEqual(lab1.modify("lab1",60,20,2),"Lab1 con 60 usuarios y 20 "
                                                   "de capacidad y tipo Materiales")
        self.assertEqual(lab2.modify("lab2",60,20,1),"Lab2 con 60 usuarios y 20 "
                                                   "de capacidad y tipo Corrosion")

    def test_labs_delete(self):
        lab1 = Labs.objects.get (pk=1)
        self.assertEqual(lab1.deactived(),"Se desactivo")

    def test_labs_create(self):
        countBefore=Labs.objects.count()
        Labs.objects.create(labname="Laboratorio antisismicos", numUser=30,
                             capacity=50, activate=True,typeLab=1)
        self.assertEqual(Labs.objects.count(),countBefore+1)

class TypeLabTest(TestCase):
    def setUp(self):
        TypeLabs.objects.create(typename="Corrosion", active=True)
        TypeLabs.objects.create(typename="Materiales", active=True)

    def test_typeLab_modify(self):
        type_lab1 = Labs.objects.get(pk=1)
        type_lab2 = Labs.objects.get(pk=2)
        self.assertEqual(type_lab1.modify("Tipo3"), "Lab1 es de Tipo3")
        self.assertEqual(type_lab2.modify("Tipo3"), "Lab2 es de Tipo3")

    def test_typelab_delete(self):
        type_lab1 = Labs.objects.get(pk=1)
        self.assertEqual(type_lab1.deactived(), "Se desactivo")

    def test_typelabs_create(self):
        countBefore = TypeLabs.objects.count()
        TypeLabs.objects.create(typename="Corrosion", active=True)
        self.assertEqual(TypeLabs.objects.count(), countBefore + 1)

## Pruebas para los tipos de ensayo
class TypeLabAssay(TestCase):
    def setUp(self):
        TypeAssay.objects.create(typename="TipoEnsayo1", active =True)
        TypeAssay.objects.create(typename="TipoEnsayo2", active =True)

    def test_typeLab_modify(self):
        type1= TypeAssay.objects.get(pk=1)
        type2= TypeAssay.objects.get(pk=2)
        self.assertEqual(type1.modify("TipoEnsayo3"),"Ensayo1 es de TipoEnsayo3")
        self.assertEqual(type2.modify("TipoEnsayo3"),"Ensayo2 es de TipoEnsayo3")

    def test_typelab_delete(self):
        type1 = TypeAssay.objects.get (pk=1)
        self.assertEqual(type1.deactived(),"Se desactivo")

    def test_typelabs_create(self):
        countBefore=TypeAssay.objects.count()
        TypeAssay.objects.create(typename="TipoEnsayo4", active=True)
        self.assertEqual(TypeAssay.objects.count(),countBefore+1)



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

    def test_typelabs_create(self):
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

    def test_typelabs_create(self):
        countBefore=TypeSample.objects.count()
        TypeSample.objects.create(typename="TipoMuestra4", active=True)
        self.assertEqual(TypeSample.objects.count(),countBefore+1)

