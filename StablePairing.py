# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 20:01:07 2021

@author: Michael Lin
"""
from collections import namedtuple
# Student will be numbered from 0 to N-1 while hospitals are numbered from N to 2 * N - 1
# An example Student: [5, 6, 4, 7]
# Hospital: [0, 1, 2, 3]


class Student:
    def __init__(self, name, pref):
        self.id = name
        if isinstance(pref, list):
            self.pref = self._check(pref)
        else:
            self.pref = None
            raise AttributeError("Need to be a list")

    def _check(self, val):
        """
        Check for repetition in preference
        :param val: preference list
        :return: None or the preference list
        """
        if len(set(val)) != len(val):
            return None
        else:
            return val


class Hospital:
    def __init__(self, name, pref):
        self.id = name
        self.visited = []
        if isinstance(pref, list):
            self.pref = self._check(pref)
        else:
            self.pref = None
            raise AttributeError("Need to be a list")

    def _check(self, val):
        """
        Check for repetition in preference
        :param val: preference list
        :return: None or the preference list
        """
        if len(set(val)) != len(val):
            return None
        else:
            return val


class PairingSystem:
    def __init__(self, student_list=[], hospital_list=[]):
        self.student_list = student_list
        self.hospital_list = hospital_list

    @property
    def student_list(self):
        return self._student_list

    @property
    def hospital_list(self):
        return self._hospital_list

    @hospital_list.setter
    def hospital_list(self, val):
        if isinstance(val, list):
            self._hospital_list = self._transform(val)
        else:
            self._hospital_list = None
            raise AttributeError("Need to be a list of student")

    @student_list.setter
    def student_list(self, val):
        if isinstance(val, list):
            self._student_list = self._transform(val)
        else:
            self._student_list = None
            raise AttributeError("Need to be a list of hospital")

    def _transform(self, val):
        """
        Transform the list into dictionary for better accessibility
        :param val: student list or hospital list
        :return: Dictionary with id as key and either Student or Hospital as value
        """
        output = {}
        for v in val:
            output[v.id] = v
        return output

    def stable_pairing(self):
        """
        Implementation of Gale-Shipley stable pairing algorithm
        :return: Stable pairing
        """
        queue = list(self.student_list.values())
        res_pairing = {}
        while queue:
            student = queue.pop(0)
            preference = student.pref
            top_choice = self.hospital_list[preference[0]]
            for p in preference:
                hospital = self.hospital_list[p]
                if student.id not in hospital.visited:
                    top_choice = hospital
                    break
            top_choice.visited.append(student.id)

            # Check if top choice is taken
            if top_choice.id not in res_pairing:
                res_pairing[top_choice.id] = student.id
            else:
                curr_pairing = self.student_list[res_pairing[top_choice.id]]
                if top_choice.pref.index(curr_pairing.id) > top_choice.pref.index(student.id):
                    # If larger index, swap the pairing and put the original one into queue
                    res_pairing[top_choice.id] = student.id
                    queue.append(curr_pairing)
                else:
                    # If smaller index, keep current pairing and don't swap
                    queue.append(student)

        return res_pairing


def main():
    student1 = Student(0, [7, 5, 6, 4])
    student2 = Student(1, [5, 4, 6, 7])
    student3 = Student(2, [4, 5, 6, 7])
    student4 = Student(3, [4, 5, 6, 7])
    students = [student1, student2, student3, student4]

    hospital1 = Hospital(4, [0, 1, 2, 3])
    hospital2 = Hospital(5, [0, 1, 2, 3])
    hospital3 = Hospital(6, [0, 1, 2, 3])
    hospital4 = Hospital(7, [0, 1, 2, 3])
    hospitals = [hospital1, hospital2, hospital3, hospital4]

    test_pairing_system = PairingSystem()
    test_pairing_system.student_list = students
    test_pairing_system.hospital_list = hospitals
    print(test_pairing_system.stable_pairing())


if __name__ == '__main__':
    main()
