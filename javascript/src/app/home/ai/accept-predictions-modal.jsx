import { useState } from 'react'
import { Checkbox, CheckboxField, CheckboxGroup } from '@/components/checkbox'
import { Dialog, DialogActions, DialogBody, DialogDescription, DialogTitle } from '@/components/dialog'
import { Description, Fieldset, Label, Legend } from '@/components/fieldset'
import { Button } from '@/components/button'

export default function AcceptPredictionsModal({ open, onClose }) {
    const [dontShowAgain, setDontShowAgain] = useState(false);

    return (
        <Dialog open={open} onClose={() => onClose(dontShowAgain)}>
            <DialogTitle>Accept AI Predictions</DialogTitle>
            <DialogDescription>
              Something about how the ai works, what you do to train the ai etc
            </DialogDescription>
        <DialogBody>
{/*              TODO: something about how the ai works */}
        </DialogBody>
        <DialogActions>
            <CheckboxGroup>
          <CheckboxField>
            <Checkbox name="discoverability" value="show_on_events_page" checked={dontShowAgain} onChange={setDontShowAgain} />
            <Label>Don't show this again</Label>
          </CheckboxField>
          </CheckboxGroup>
          <Button onClick={() => onClose(dontShowAgain)}>Ok</Button>
        </DialogActions>
      </Dialog>
    )
}