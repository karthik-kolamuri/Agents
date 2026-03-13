import asyncio
from agno.workflow import Workflow, StepOutput

async def async_step(step_input):
    await asyncio.sleep(0.1)
    return StepOutput(content=f"Async: {step_input.input}")

wf = Workflow(name="test_async", steps=[async_step])

async def main():
    try:
        response = await wf.arun({"input": "Hello"})
        print(f"Success: {getattr(response, 'content', response)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
