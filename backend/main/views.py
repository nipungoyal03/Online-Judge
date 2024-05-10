from rest_framework import generics
from main.models import Problem,TestCase,Solution
from main.serializers import ProblemSerializer
import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import uuid
import os
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication



class ProblemListAPIView(generics.ListAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    authentication_classes = [JWTAuthentication]  # Use JWT authentication
    permission_classes = [IsAuthenticated]  # Require authentication to access the API


class ProblemDetailAPIView(generics.RetrieveAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    lookup_field = "code"

    authentication_classes = [JWTAuthentication]  # Use JWT authentication
    permission_classes = [IsAuthenticated]


class ExecuteCodeAPIView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWT authentication
    permission_classes = [IsAuthenticated]

    def post(self, request):
        lang = request.data.get("lang")
        problem_code = request.data.get("problem_code")
        code = request.data.get("code")

        if lang not in ["c", "cpp", "py"]:
            return Response(
                {"error": "Invalid language"}, status=status.HTTP_400_BAD_REQUEST
            )

        folder_name = "InputCodes"

        os.makedirs(folder_name, exist_ok=True)
        os.makedirs("GeneratedOutput", exist_ok=True)

        curr_dir = os.getcwd()
        folder_path = os.path.join(curr_dir, folder_name)
        uniquename = uuid.uuid4().hex
        unique_filename = f"{uniquename}.{lang}"
        file_path = os.path.join(folder_path, unique_filename)

        with open(file_path, "w") as f:
            f.write(code)
        os.chdir(folder_path)

        problem = Problem.objects.filter(code=problem_code).first()
        test_case = TestCase.objects.filter(problem=problem).first()
        input_path=test_case.input
        output_path=test_case.output
        # print(input_path)
        # print(output_path)

        try:
            if lang == "c":
                # On Mac, use clang instead of gcc for compiling C code
                result = subprocess.run(
                    ["clang", f"{unique_filename}", "-o", uniquename]
                )
                if result.returncode == 0:
                    os.chdir(curr_dir)
                    print(os.getcwd())
                    # On Mac, execute the compiled executable with input redirection and output file
                    with open(f"{input_path}", "r") as input_file:
                        with open(
                            f"./GeneratedOutput/{uniquename}.txt", "w"
                        ) as output_file:
                            output = subprocess.run(
                                [f"./InputCodes/{uniquename}"],
                                stdin=input_file,
                                stdout=output_file,
                            )

            elif lang == "cpp":
                result = subprocess.run(
                    ["clang++", f"{unique_filename}", "-o", uniquename]
                )
                if result.returncode == 0:
                    os.chdir(curr_dir)
                    print(os.getcwd())
                    # Create GeneratedOutput directory if it doesn't exist
                    generated_output_dir = "./GeneratedOutput"
                    os.makedirs(generated_output_dir, exist_ok=True)
                    # On Mac, execute the compiled executable with input redirection and output file
                    with open(f"{input_path}", "r") as input_file:
                        output_file_path = f"./GeneratedOutput/{uniquename}.txt"
                        with open(output_file_path, "w") as output_file:
                            subprocess.run(
                                [f"./InputCodes/{uniquename}"],
                                stdin=input_file,
                                stdout=output_file,
                            )

            elif lang == "py":
                os.chdir(curr_dir)
                print(os.getcwd())
                # On Mac, execute the Python script with input redirection and output file
                with open(f"{input_path}", "r") as input_file:
                    output_file_path = f"./GeneratedOutput/{uniquename}.txt"
                    with open(output_file_path, "w") as output_file:
                        subprocess.run(
                            ["python3", f"InputCodes/{uniquename}.py"],
                            stdin=input_file,
                            stdout=output_file,
                        )

            with open(f"GeneratedOutput/{uniquename}.txt", "r") as gen_file:
                generated_output = gen_file.read()
            with open(f"{output_path}", "r") as ref_file:
                reference_output = ref_file.read()
                # Compare the contents of the files
            verdict = "Accepted" if generated_output.strip() == reference_output.strip() else "Wrong Answer"

            # Create a Solution instance and save it to the database
            solution = Solution.objects.create(
                problem=problem,
                verdict=verdict
            )

            return Response(
                {"output": generated_output, "result": verdict},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
