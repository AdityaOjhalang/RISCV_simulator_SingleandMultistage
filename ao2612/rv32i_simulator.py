import copy
import os
from riscvmodel.code import decode, MachineDecodeError
from riscvmodel.isa import Instruction

from instructions import get_instruction_class, InstructionBase, ADDERBTYPE, ADDERJTYPE
from models import InsMem, DataMem, RegisterFile, State

# memory size, in reality, the memory size should be 2^32, but for this lab, for the space reason
# we keep it as this large number, but the memory is still 32-bit addressable.
MemSize = 1000


class Core(object):
    def __init__(self, ioDir: str, imem: InsMem, dmem: DataMem):
        self.myRF = RegisterFile(ioDir)
        self.cycle = 0
        self.halted = False
        self.ioDir = ioDir
        self.state = State()
        self.state.nop_init()
        self.nextState = State()
        self.nextState.nop_init()
        self.ext_imem: InsMem = imem
        self.ext_dmem: DataMem = dmem

    def calculate_performance_metrics(self, output_path):
            # Performance metrics calculations
            cpi = float(self.cycle) / self.state.IF.instruction_count if self.state.IF.instruction_count else float('inf')
            ipc = 1.0 / cpi if cpi != float('inf') else 0.0

            result_format = f"{self.stages} Core Performance Metrics-----------------------------\n" \
                            f"Instructions: {self.state.IF.instruction_count}\n"\
                            f"Number of cycles taken: {self.cycle}\n" \
                            f"Cycles per instruction: {cpi:.2f}\n" \
                            f"Instructions per cycle: {ipc:.2f}\n"

            # Use the output_path parameter to determine the output file path
            performance_metrics_file_path = os.path.join(output_path, "PerformanceMetrics_Result.txt")

            # Writing performance metrics to the file
            write_mode = "w" if self.stages == "Single Stage" else "a"
            with open(performance_metrics_file_path, write_mode) as file:
                file.write(result_format)

            print(f"Performance metrics saved to {performance_metrics_file_path}")


class SingleStageCore(Core):
    def __init__(self, output_dir: str, imem: InsMem, dmem: DataMem):
        super(SingleStageCore, self).__init__(os.path.join(output_dir, "SS_"), imem, dmem)
        # Now use output_dir to form the path to StateResult_SS.txt
        self.opFilePath = os.path.join(output_dir, "StateResult_SS.txt")
        self.stages = "Single Stage"
        # Make sure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.stages = "Single Stage"

    def step(self):
        # IF
        instruction_bytes = self.ext_imem.read_instr(self.state.IF.PC)
        if instruction_bytes == "1" * 32:
            self.nextState.IF.nop = True
        else:
            self.nextState.IF.PC += 4
            self.nextState.IF.instruction_count = self.nextState.IF.instruction_count + 1

        try:
            # ID
            instruction: Instruction = decode(int(instruction_bytes, 2))
            if instruction.mnemonic in ['beq', 'bne']:
                self.nextState.IF.PC = ADDERBTYPE(instruction, self.state, self.myRF).get_pc()
            elif instruction.mnemonic == 'jal':
                self.nextState.IF.PC = ADDERJTYPE(instruction, self.state, self.myRF).get_pc()
            else:
                instruction_ob: InstructionBase = get_instruction_class(instruction.mnemonic)(instruction, self.ext_dmem, self.myRF,self.state,self.nextState)
                # Ex
                alu_result = instruction_ob.execute()
                # Load/Store (MEM)
                mem_result = instruction_ob.mem(alu_result=alu_result)
                # WB
                wb_result = instruction_ob.wb(mem_result=mem_result, alu_result=alu_result)
        except MachineDecodeError as e:
            if "{:08x}".format(e.word) == 'ffffffff':
                pass
            else:
                raise Exception("Invalid Instruction to Decode")
        # self.halted = True
        if self.state.IF.nop:
            self.nextState.IF.instruction_count = self.nextState.IF.instruction_count + 1
            self.halted = True

        self.myRF.output_rf(self.cycle)  # dump RF
        self.printState(self.nextState, self.cycle)  # print states after executing cycle 0, cycle 1, cycle 2 ...

        # The end of the cycle and updates the current state with the values calculated in this cycle
        self.state = copy.deepcopy(self.nextState)
        # self.nextState = copy.deepcopy(self.nextState)
        self.cycle += 1

    def printState(self, state, cycle):
        printstate = ["-" * 70 + "\n", "State after executing cycle: " + str(cycle) + "\n"]
        printstate.append("IF.PC: " + str(state.IF.PC) + "\n")
        printstate.append("IF.nop: " + str(state.IF.nop) + "\n")

        if (cycle == 0):
            perm = "w"
        else:
            perm = "a"
        with open(self.opFilePath, perm) as wf:
            wf.writelines(printstate)

if __name__ == "__main__":
    pass
