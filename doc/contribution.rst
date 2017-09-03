#############
Contribution
#############

***********
Code Style
***********

Naming conversions
===================

Still not written in stone but the ``snake_case`` seems to dominate the code base.
If you are new to the project, take up that one.

Most importantly, use descriptive names and stick to one style and use it consequently.

Regarding functions, variables, class etc. we follow the good advices of PEP8_.

.. note::
  Functions: Please use an underscore like ``_spam_and_helps()`` for functions which should not be used outside of the sub-package (package). |br| Start function names without an underscore if they are meant to be used outside of the package/sub-package. E. g. ``flying_circus()``.

For the rest, it is still to be defined. But we basically follow PEP8_,  but do not forget how PEP8_ itself starts:

  *"A Foolish Consistency is the Hobgoblin of Little Minds"*
 
So use it when it makes sense, and do not where it does not.
We would even suggest to look for an auto-pep8 plug-in for your favourite IDE or text editor. Or go bare bones and get something like flake8_ to check your code. If it is too annoying, you can always add some guidelines to be ignored. But


.. todo::
  Look into ``rivus.main.rivus`` and reformat code where it makes sense.
  (Mathematical notation vs. descriptiveness)

.. _PEP8: http://legacy.python.org/dev/peps/pep-0008/
.. _flake8: http://flake8.pycqa.org/en/latest/

**********
Unittests
**********

.. todo::
  - Why and how-to
    - Workflow
  - Future critera for PR acceptance

**********
Profiling
**********

.. todo::
  - Why and how-to
    - Workflow
  - Bonus points at PR acceptance

**************
Documentation
**************

Nobody can explain better what your code does than you.
The docstring in the source code are elementary, and I would not suppose anybody
would submit code without it...
But to make it easier for the next contributors, this online documentation is to be maintained as well.
Please take the time and jump into the following short tutorial and ensure the success of your contribution
with a nice documentation.

.. todo::
  - RtD & Sphinx: Why and how-to
    - Workflow
      - conversion tools
  - Kinda needed at PR acceptance

**************
Doc TODOs
**************
Summary of the ToDos from the *whole* documentation.

.. todolist::
