from django.test import TestCase
from ..models import Labs

class LabsTestCase(TestCase):
    def setUp(self):
        Labs.objects.create(labname="Laboratorio de Corrosion", numUser=30,
                            capacity=50,activate=True)
        Labs.objects.create(labname="Laboratorio de Materiales", numUser=32,
                            capacity=60,activate=True)

    def test_labs_modify(self):
        lab1= Labs.objects.get(pk=1)
        lab2= Labs.objects.get(pk=2)
        self.assertEqual(lab1.modify("lab1",60,20),"Lab1 con 60 usuarios y 20 "
                                                   "de capacidad")
        self.assertEqual(lab2.modify("lab2",60,20),"Lab2 con 60 usuarios y 20 "
                                                   "de capacidad")

    def test_labs_delete(self):
        lab1 = Labs.objects.get (pk=1)
        self.assertEqual(lab1.deactived(),"Se desactivo")

    def test_labs_create(self):
        countBefore=Labs.objects.count()
        Labs.objects.create(labname="Laboratorio antisismicos", numUser=30,
                             capacity=50, activate=True)
        self.assertEqual(Labs.objects.count(),countBefore+1)

    def test_labs_
